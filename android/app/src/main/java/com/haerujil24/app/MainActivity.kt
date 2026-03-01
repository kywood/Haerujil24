package com.haerujil24.app

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.*
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.channels.FileChannel
import java.util.concurrent.Executors

import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas

// RenderScript (deprecated but dev/test에서 빠르고 안정적)
import android.renderscript.Allocation
import android.renderscript.Element
import android.renderscript.RenderScript
import android.renderscript.ScriptIntrinsicYuvToRGB

class MainActivity : ComponentActivity() {

    private val requestPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            Log.i("CameraX", "Camera permission granted=$granted")
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermission.launch(Manifest.permission.CAMERA)
        }

        setContent {
            MaterialTheme {
                Surface(Modifier.fillMaxSize()) {
                    CameraWithOverlay()
                }
            }
        }
    }
}

// -------------------- UI + Camera --------------------

@Composable
private fun CameraWithOverlay() {
    val context = LocalContext.current
    val mainExecutor = remember { ContextCompat.getMainExecutor(context) }

    var errorText by remember { mutableStateOf<String?>(null) }

    // ✅ 모델 입력(640) 기준 좌표로 나온 박스들
    var boxes by remember { mutableStateOf<List<DetBox>>(emptyList()) }

    // ✅ 추론에 실제 사용된 소스(회전 반영 후) 프레임 크기
    var srcW by remember { mutableIntStateOf(0) }
    var srcH by remember { mutableIntStateOf(0) }

    val analysisExecutor = remember { Executors.newSingleThreadExecutor() }
    val yuvToRgb = remember { YuvToRgbConverter(context) }

    val inputSize = 640

    // TFLite 로딩 (1회)
    val interpreter = remember {
        try {
            val fd = context.assets.openFd("best_float16.tflite")
            FileInputStream(fd.fileDescriptor).use { input ->
                val ch = input.channel
                val model = ch.map(FileChannel.MapMode.READ_ONLY, fd.startOffset, fd.declaredLength)
                Log.i("YOLO", "model loaded: best_float16.tflite size=${fd.declaredLength}")
                Interpreter(model, Interpreter.Options().setNumThreads(4))
            }
        } catch (e: Exception) {
            Log.e("YOLO", "model load FAILED", e)
            null
        }
    }

    // 재사용 메모리
    val srcBitmap = remember { Bitmap.createBitmap(1280, 720, Bitmap.Config.ARGB_8888) } // 임시, 실제로는 아래에서 맞춤
    val rotatedBitmap = remember { Bitmap.createBitmap(1280, 720, Bitmap.Config.ARGB_8888) } // 임시
    val inputBitmap = remember { Bitmap.createBitmap(inputSize, inputSize, Bitmap.Config.ARGB_8888) }
    val inputBuffer = remember { ByteBuffer.allocateDirect(4 * inputSize * inputSize * 3).order(ByteOrder.nativeOrder()) }
    val output = remember { Array(1) { Array(84) { FloatArray(8400) } } }

    var loggedIo by remember { mutableStateOf(false) }

    // 로그/추론 throttle
    var lastAliveLog by remember { mutableStateOf(0L) }
    var lastInferTs by remember { mutableStateOf(0L) }
    val inferIntervalMs = 200L

    DisposableEffect(Unit) {
        onDispose {
            runCatching { analysisExecutor.shutdown() }
            runCatching { yuvToRgb.close() }
            runCatching { interpreter?.close() }
        }
    }

    Column(Modifier.fillMaxSize()) {
        if (errorText != null) {
            Text(
                text = errorText!!,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(16.dp)
            )
        }

        Box(Modifier.fillMaxSize()) {

            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { ctx ->
                    PreviewView(ctx).apply {
                        // ✅ 여기랑 오버레이 매핑이 같은 규칙이어야 함
                        scaleType = PreviewView.ScaleType.FIT_CENTER
                        implementationMode = PreviewView.ImplementationMode.COMPATIBLE
                    }
                },
                update = { previewView ->
                    val cameraProviderFuture = ProcessCameraProvider.getInstance(context)
                    cameraProviderFuture.addListener({
                        runCatching {
                            val cameraProvider = cameraProviderFuture.get()

                            val preview = Preview.Builder().build().also { p ->
                                p.setSurfaceProvider(previewView.surfaceProvider)
                            }

                            val imageAnalysis = ImageAnalysis.Builder()
                                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                                .build()
                                .also { analysis ->
                                    analysis.setAnalyzer(analysisExecutor) { imageProxy ->
                                        try {
                                            val tflite = interpreter ?: run {
                                                imageProxy.close()
                                                return@setAnalyzer
                                            }

                                            val now = System.currentTimeMillis()
                                            if (now - lastAliveLog >= 1000) {
                                                lastAliveLog = now
                                                Log.d("YOLO", "analyzer alive rot=${imageProxy.imageInfo.rotationDegrees}")
                                            }

                                            // 1) ImageProxy -> Bitmap (원본 크기)
                                            val w = imageProxy.width
                                            val h = imageProxy.height
                                            val tmpSrc = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
                                            yuvToRgb.yuvToRgb(imageProxy, tmpSrc)

                                            // 2) rotation 반영해서 “똑바른” 프레임 만들기
                                            val rot = imageProxy.imageInfo.rotationDegrees
                                            val upright = rotateBitmap(tmpSrc, rot)

                                            // ✅ 추론 기준 src 크기 저장 (오버레이 변환에 사용)
                                            srcW = upright.width
                                            srcH = upright.height

                                            // 3) 센터크롭 + 640 리사이즈 (letterbox 없이)
                                            centerCropToSquareAndResize(upright, inputBitmap, inputSize)

                                            // 4) IO 로그 1회
                                            if (!loggedIo) {
                                                val inT = tflite.getInputTensor(0)
                                                val outT = tflite.getOutputTensor(0)
                                                Log.i("YOLO", "input=${inT.shape().contentToString()} type=${inT.dataType()}")
                                                Log.i("YOLO", "output=${outT.shape().contentToString()} type=${outT.dataType()}")
                                                loggedIo = true
                                            }

                                            // 5) throttle
                                            if (now - lastInferTs < inferIntervalMs) return@setAnalyzer
                                            lastInferTs = now

                                            // 6) preprocess
                                            bitmapToFloatBufferNHWC(inputBitmap, inputSize, inputBuffer)

                                            // 7) inference
                                            tflite.run(inputBuffer, output)

                                            // 8) decode
                                            val dets = decodeYoloV8_84_8400(
                                                out = output,
                                                confThreshold = 0.20f,
                                                iouThreshold = 0.45f,
                                                maxDet = 20
                                            )

                                            mainExecutor.execute {
                                                boxes = dets
                                            }
                                        } catch (e: Exception) {
                                            Log.e("YOLO", "analyze/infer fail", e)
                                        } finally {
                                            imageProxy.close()
                                        }
                                    }
                                }

                            cameraProvider.unbindAll()
                            cameraProvider.bindToLifecycle(
                                context as ComponentActivity,
                                CameraSelector.DEFAULT_BACK_CAMERA,
                                preview,
                                imageAnalysis
                            )
                        }.onFailure { e ->
                            errorText = "카메라 시작 실패: ${e.message}"
                            Log.e("CameraX", "bind failed", e)
                        }
                    }, mainExecutor)
                }
            )

            // --------------- Overlay ---------------
            DetectionOverlayFitCenter(
                modifier = Modifier.fillMaxSize(),
                boxes = boxes,
                // ✅ 이 값이 “추론 전에 upright 프레임에서 센터크롭한 영역”을 의미
                srcW = srcW,
                srcH = srcH,
                inputSize = inputSize
            )
        }
    }
}

// -------------------- Overlay (FIT_CENTER + CenterCrop rule) --------------------

@Composable
private fun DetectionOverlayFitCenter(
    modifier: Modifier,
    boxes: List<DetBox>,
    srcW: Int,
    srcH: Int,
    inputSize: Int
) {
    Canvas(modifier = modifier) {
        if (srcW <= 0 || srcH <= 0) return@Canvas

        val viewW = size.width
        val viewH = size.height

        // ✅ 1) upright(srcW,srcH)에서 우리가 센터크롭한 정사각형 영역 계산
        val cropSize = minOf(srcW, srcH).toFloat()
        val cropLeft = (srcW - cropSize) / 2f
        val cropTop = (srcH - cropSize) / 2f

        // ✅ 2) 그 crop 정사각형이 PreviewView(FIT_CENTER)에서 어떻게 보이는지 계산
        // FIT_CENTER: 전체 뷰 안에 cropSize x cropSize 가 “비율 유지”로 들어감
        val scale = minOf(viewW / cropSize, viewH / cropSize)
        val dx = (viewW - cropSize * scale) / 2f
        val dy = (viewH - cropSize * scale) / 2f

        // ✅ Paint는 루프 밖에서 1번만 만들기 (매 프레임/매 박스 생성 방지)
        val textPaint = android.graphics.Paint().apply {
            isAntiAlias = true
            color = android.graphics.Color.GREEN
            textSize = 36f
            style = android.graphics.Paint.Style.FILL
            typeface = android.graphics.Typeface.create(
                android.graphics.Typeface.DEFAULT,
                android.graphics.Typeface.BOLD
            )
        }
        val bgPaint = android.graphics.Paint().apply {
            isAntiAlias = true
            color = android.graphics.Color.argb(160, 0, 0, 0) // 반투명 검정
            style = android.graphics.Paint.Style.FILL
        }

        for (b in boxes) {
            // b는 0..640 좌표(정사각형 input 기준)
            // input(640) -> cropSize로 역스케일
            val x1 = cropLeft + (b.left / inputSize) * cropSize
            val y1 = cropTop + (b.top / inputSize) * cropSize
            val x2 = cropLeft + (b.right / inputSize) * cropSize
            val y2 = cropTop + (b.bottom / inputSize) * cropSize

            // crop 좌표 -> view 좌표
            val left = dx + (x1 - cropLeft) * scale
            val top = dy + (y1 - cropTop) * scale
            val w = (x2 - x1) * scale
            val h = (y2 - y1) * scale

            // 박스
            drawRect(
                color = Color.Green,
                topLeft = Offset(left, top),
                size = Size(w, h),
                style = Stroke(width = 3f)
            )

            // ✅ 라벨링(간단): cls + score
            // Canvas 텍스트는 Compose 기본 Canvas에서 바로 그리기 까다로워서
            // “일단 박스만 정확히 맞춘 뒤”, 다음 단계에서 AndroidCanvas로 텍스트 그려줄게.


            // ✅ 라벨 (cls + score)
            val className = if (b.cls in COCO_CLASSES.indices)
                COCO_CLASSES[b.cls]
            else
                "cls=${b.cls}"

            val label = "$className ${"%.2f".format(b.score)}"

//            val label = "cls=${b.cls} ${"%.2f".format(b.score)}"
            val pad = 8f
            val textW = textPaint.measureText(label)
            val textH = (textPaint.fontMetrics.bottom - textPaint.fontMetrics.top)

            // 박스 위에 표시(위가 화면 밖이면 박스 안쪽으로)
            val tx = left
            val ty = if (top - (textH + pad * 2f) >= 0f) top - 6f else top + textH + pad

            drawIntoCanvas { canvas ->
                val nc = canvas.nativeCanvas

                // 배경
                val bg = android.graphics.RectF(
                    tx,
                    ty - textH - pad,
                    tx + textW + pad * 2f,
                    ty + pad
                )
                nc.drawRoundRect(bg, 8f, 8f, bgPaint)

                // 텍스트
                nc.drawText(label, tx + pad, ty, textPaint)
            }

        }
    }
}

// -------------------- YOLO Decode --------------------

private fun decodeYoloV8_84_8400(
    out: Array<Array<FloatArray>>,
    confThreshold: Float,
    iouThreshold: Float,
    maxDet: Int
): List<DetBox> {
    val numBoxes = 8400
    val numClasses = 80
    val inputSize = 640f

    val candidates = ArrayList<DetBox>(128)

    for (i in 0 until numBoxes) {
        val rawCx = out[0][0][i]
        val rawCy = out[0][1][i]
        val rawW = out[0][2][i]
        val rawH = out[0][3][i]

        val isNormalized = rawW <= 2f && rawH <= 2f && rawCx <= 1.2f && rawCy <= 1.2f
        val cx = if (isNormalized) rawCx * inputSize else rawCx
        val cy = if (isNormalized) rawCy * inputSize else rawCy
        val w = if (isNormalized) rawW * inputSize else rawW
        val h = if (isNormalized) rawH * inputSize else rawH

        var bestC = -1
        var bestScore = 0f
        for (c in 0 until numClasses) {
            val score = out[0][4 + c][i]
            if (score > bestScore) {
                bestScore = score
                bestC = c
            }
        }

        if (bestScore < confThreshold) continue

        val left = (cx - w / 2f).coerceIn(0f, inputSize)
        val top = (cy - h / 2f).coerceIn(0f, inputSize)
        val right = (cx + w / 2f).coerceIn(0f, inputSize)
        val bottom = (cy + h / 2f).coerceIn(0f, inputSize)

        if ((right - left) < 2f || (bottom - top) < 2f) continue

        candidates.add(DetBox(left, top, right, bottom, bestScore, bestC))
    }

    candidates.sortByDescending { it.score }

    val selected = ArrayList<DetBox>(maxDet)
    for (cand in candidates) {
        var keep = true
        for (sel in selected) {
            if (iou(cand, sel) > iouThreshold) {
                keep = false
                break
            }
        }
        if (keep) {
            selected.add(cand)
            if (selected.size >= maxDet) break
        }
    }
    return selected
}

private fun iou(a: DetBox, b: DetBox): Float {
    val interLeft = maxOf(a.left, b.left)
    val interTop = maxOf(a.top, b.top)
    val interRight = minOf(a.right, b.right)
    val interBottom = minOf(a.bottom, b.bottom)

    val interW = (interRight - interLeft).coerceAtLeast(0f)
    val interH = (interBottom - interTop).coerceAtLeast(0f)
    val interArea = interW * interH

    val areaA = (a.right - a.left).coerceAtLeast(0f) * (a.bottom - a.top).coerceAtLeast(0f)
    val areaB = (b.right - b.left).coerceAtLeast(0f) * (b.bottom - b.top).coerceAtLeast(0f)
    val union = areaA + areaB - interArea
    return if (union <= 0f) 0f else interArea / union
}

data class DetBox(
    val left: Float,
    val top: Float,
    val right: Float,
    val bottom: Float,
    val score: Float,
    val cls: Int
)

// ✅ 여기 추가
private val COCO_CLASSES = arrayOf(
    "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
    "traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
    "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
    "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
    "kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
    "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
    "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake",
    "chair","couch","potted plant","bed","dining table","toilet","tv","laptop",
    "mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink",
    "refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"
)

// -------------------- Preprocess --------------------

private fun bitmapToFloatBufferNHWC(src: Bitmap, size: Int, out: ByteBuffer) {
    out.rewind()
    val pixels = IntArray(size * size)
    src.getPixels(pixels, 0, size, 0, 0, size, size)

    for (px in pixels) {
        val r = ((px shr 16) and 0xFF) / 255f
        val g = ((px shr 8) and 0xFF) / 255f
        val b = (px and 0xFF) / 255f
        out.putFloat(r); out.putFloat(g); out.putFloat(b)
    }
    out.rewind()
}

// -------------------- Image Utils --------------------

private fun rotateBitmap(src: Bitmap, degrees: Int): Bitmap {
    if (degrees == 0) return src
    val m = Matrix().apply { postRotate(degrees.toFloat()) }
    return Bitmap.createBitmap(src, 0, 0, src.width, src.height, m, true)
}

/**
 * upright bitmap에서 센터크롭 정사각형을 만든 다음, dst(640x640)에 리사이즈로 복사.
 */
private fun centerCropToSquareAndResize(upright: Bitmap, dst: Bitmap, size: Int) {
    val w = upright.width
    val h = upright.height
    val crop = minOf(w, h)
    val left = (w - crop) / 2
    val top = (h - crop) / 2

    val srcRect = Rect(left, top, left + crop, top + crop)
    val dstRect = Rect(0, 0, size, size)

    val canvas = Canvas(dst)
    canvas.drawBitmap(upright, srcRect, dstRect, null)
}

// -------------------- YUV -> RGB --------------------

private class YuvToRgbConverter(context: Context) {
    private val rs: RenderScript = RenderScript.create(context)
    private val script: ScriptIntrinsicYuvToRGB = ScriptIntrinsicYuvToRGB.create(rs, Element.U8_4(rs))

    private var inputAllocation: Allocation? = null
    private var outputAllocation: Allocation? = null
    private var lastInputSize = 0

    fun yuvToRgb(image: ImageProxy, output: Bitmap) {
        val nv21 = yuv420ToNv21(image)

        if (inputAllocation == null || lastInputSize != nv21.size) {
            inputAllocation?.destroy()
            inputAllocation = Allocation.createSized(rs, Element.U8(rs), nv21.size)
            lastInputSize = nv21.size
        }

        if (outputAllocation == null || outputAllocation?.type?.x != output.width || outputAllocation?.type?.y != output.height) {
            outputAllocation?.destroy()
            outputAllocation = Allocation.createFromBitmap(rs, output)
        }

        inputAllocation!!.copyFrom(nv21)
        script.setInput(inputAllocation)
        script.forEach(outputAllocation)
        outputAllocation!!.copyTo(output)
    }

    fun close() {
        runCatching { inputAllocation?.destroy() }
        runCatching { outputAllocation?.destroy() }
        runCatching { script.destroy() }
        runCatching { rs.destroy() }
    }

    private fun yuv420ToNv21(image: ImageProxy): ByteArray {
        val yBuffer = image.planes[0].buffer
        val uBuffer = image.planes[1].buffer
        val vBuffer = image.planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)
        yBuffer.get(nv21, 0, ySize)

        val chromaHeight = image.height / 2
        val chromaWidth = image.width / 2
        val uRowStride = image.planes[1].rowStride
        val vRowStride = image.planes[2].rowStride
        val uPixelStride = image.planes[1].pixelStride
        val vPixelStride = image.planes[2].pixelStride

        val uBytes = ByteArray(uSize).also { uBuffer.get(it) }
        val vBytes = ByteArray(vSize).also { vBuffer.get(it) }

        var offset = ySize
        for (row in 0 until chromaHeight) {
            for (col in 0 until chromaWidth) {
                val vIndex = row * vRowStride + col * vPixelStride
                val uIndex = row * uRowStride + col * uPixelStride
                nv21[offset++] = vBytes[vIndex]
                nv21[offset++] = uBytes[uIndex]
            }
        }
        return nv21
    }
}