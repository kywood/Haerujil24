package com.haerujil24.app.camera

import android.content.Context
import android.graphics.Bitmap
import android.renderscript.Allocation
import android.renderscript.Element
import android.renderscript.RenderScript
import android.renderscript.ScriptIntrinsicYuvToRGB
import android.renderscript.Type
import androidx.camera.core.ImageProxy
import java.nio.ByteBuffer

/**
 * NOTE: RenderScript는 deprecated지만, CameraX 샘플에서도 여전히 “가장 호환 좋은” 변환기로 많이 씀.
 * API 24+에서 잘 동작.
 */
class YuvToRgbConverter(context: Context) {
    private val rs: RenderScript = RenderScript.create(context)
    private val script: ScriptIntrinsicYuvToRGB = ScriptIntrinsicYuvToRGB.create(rs, Element.U8_4(rs))

    private var yuvBytes: ByteArray? = null
    private var inputAllocation: Allocation? = null
    private var outputAllocation: Allocation? = null

    fun yuvToRgb(image: ImageProxy, output: Bitmap) {
        val yuvBuffer = yuv420ToNv21(image)
        if (yuvBytes == null || yuvBytes!!.size != yuvBuffer.size) {
            yuvBytes = ByteArray(yuvBuffer.size)
        }
        System.arraycopy(yuvBuffer, 0, yuvBytes!!, 0, yuvBuffer.size)

        val yuvType = Type.Builder(rs, Element.U8(rs)).setX(yuvBytes!!.size)
        inputAllocation = Allocation.createTyped(rs, yuvType.create(), Allocation.USAGE_SCRIPT)

        val rgbaType = Type.Builder(rs, Element.RGBA_8888(rs)).setX(output.width).setY(output.height)
        outputAllocation = Allocation.createTyped(rs, rgbaType.create(), Allocation.USAGE_SCRIPT)

        inputAllocation!!.copyFrom(yuvBytes)
        script.setInput(inputAllocation)
        script.forEach(outputAllocation)
        outputAllocation!!.copyTo(output)
    }

    private fun yuv420ToNv21(image: ImageProxy): ByteArray {
        val yPlane = image.planes[0].buffer
        val uPlane = image.planes[1].buffer
        val vPlane = image.planes[2].buffer

        val ySize = yPlane.remaining()
        val uSize = uPlane.remaining()
        val vSize = vPlane.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)

        // Y
        yPlane.get(nv21, 0, ySize)

        // VU (NV21)
        val chromaHeight = image.height / 2
        val chromaWidth = image.width / 2

        val uRowStride = image.planes[1].rowStride
        val vRowStride = image.planes[2].rowStride
        val uPixelStride = image.planes[1].pixelStride
        val vPixelStride = image.planes[2].pixelStride

        var offset = ySize
        val uBuffer = duplicate(uPlane)
        val vBuffer = duplicate(vPlane)

        for (row in 0 until chromaHeight) {
            for (col in 0 until chromaWidth) {
                val vIndex = row * vRowStride + col * vPixelStride
                val uIndex = row * uRowStride + col * uPixelStride
                nv21[offset++] = vBuffer[vIndex]
                nv21[offset++] = uBuffer[uIndex]
            }
        }
        return nv21
    }

    private fun duplicate(buffer: ByteBuffer): ByteArray {
        val dup = buffer.duplicate()
        val arr = ByteArray(dup.remaining())
        dup.get(arr)
        return arr
    }
}