from common_lib.Thread.abThreadingControlled import abThreadingControlled


class NormalThread(abThreadingControlled):

    def __init__(self,thread_controller):
        super().__init__(thread_controller=thread_controller ,
                         name="NormalThread",
                         sleep_time=3)
        pass

    def Action(self):
        print("NormalThread ")

        ## v파일있는지 확인
        ## 있다면 가지고 와서
        ## 그런다음 파일을 ...
        ##





        pass


    pass