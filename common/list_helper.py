
"""
    import方式：
        from common import list_helper
"""

from common.ConcurrentQueue import ConcQueue



class comonQueue(ConcQueue):

    def __init__(self,num):
        super().__init__(num)

    def put(self,data):
        super().put(data)

    def get(self):
        return super().get()

class DataHelper:

    @staticmethod
    def pushData(listQue,data):
        #print('start push')

        if isinstance(listQue, ConcQueue) == False:
            return -1

        try:
            listQue.put(data)
        except Exception as e:
            print('pushData Error:', e)
            return -1
        else:
            #print('push data ok')
            return 0

    @staticmethod
    def PopData(listQue):
        if isinstance(listQue, ConcQueue) == False:
            return None
        try:
            #print('PopData get data')
            #data = dataQue.get(block=True)
            item = listQue.get()
        except Exception as e:
            print('PopData Error:', e)
            return None
        else:
            #print('Pop data ok:',data)
            return item

    @staticmethod
    def clearData(listQue):
        listQue.clear()

    @staticmethod
    def isEmpty(listQue):
        return listQue.empty()


class ListHelper():
    @staticmethod
    def find_all(target , condition):
        """
        :param target: 查找范围
        :param condition:  可以lambda 定义条件匿名函数
        :return:
        """
        for item in target:
            if condition():
                yield item

    @staticmethod
    def select(target, condition):
        for item in target:
            yield condition(item)

if __name__ == '__main__':
    dataQue = comonQueue(100)
    DataHelper.pushData(dataQue,"hello")
    print(DataHelper.PopData(dataQue))