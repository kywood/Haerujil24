from common_lib.Thread.abThreading import abThreading
from common_lib.Thread.abThreadingControlled import abThreadingControlled


class tht(abThreadingControlled):


    def __init__(self,thread_controller):
        super().__init__(thread_controller,"a")
        pass



    def Action(self):
        print("tht ")
        pass

    pass


def main():
    from common_lib.Thread.ThreadController import ThreadController
    tc = ThreadController()

    th = tht(tc)

    tc.append(th)
    tc.Start()


    pass



if __name__ == '__main__':
    main()