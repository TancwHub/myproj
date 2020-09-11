
from urllib3 import encode_multipart_formdata
import requests
import os


class requestClient():
    @staticmethod
    def post_formdata(url,data,headers=None,filepath=None):
        if (headers==None):
            header = {
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br"
            }
        else:
            header = headers
        if filepath != None:
            filepathNoname, fileName = os.path.split(filepath)
            data['file'] = (fileName, open(filepath, 'rb').read())

        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header['Content-Type'] = encode_data[1]
        res = requests.post(url, data=data, headers=header)
        #print(res)  # 转为字典格式
        return res.json()

if __name__ == "__main__":
    import base64
    data = {"password": "12345678",
             "person_uuid": "12423525",
             "card_no": "1111",
             "name": "tancw"
             }
    # url="http://192.168.1.107:8090/v1/people/add"
    # ret = requestClient.post(url,data,"D:/工作文档资料/test.jpg")
    # print(ret)

    with open("D:/工作文档资料/test.jpg", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        print('s:', base64_data , type(base64_data))
        s = base64_data.decode()
        print('s:',s,type(s))

    data1 = {"password": "12345678",
             "person_uuid": "12423525",
             "card_no": "1111",
             "name": "tancw",
             "base64img":s,
             #"file": ('test.jpg', open("D:/工作文档资料/test.jpg", 'rb').read())
             }
    print('data:',data1)
    url="http://192.168.1.107:8090/v1/people/add_by_base64img"
    ret = requestClient.post_formdata(url,data1)
    print(ret)

