""" Created by MrBBS - 4/4/2023 """
# -*-encoding:utf-8-*-

from .auto_android_adb import Device, Element

if __name__ == '__main__':
    device = Device('127.0.0.1:21503')
    # edt_search = device.findElementByText('Tìm kiếm')
    # edt_search.sendText('0762645706')
    #
    # container = device.waitElement(attr='text', value='Tìm bạn qua số điện thoại (1)')
    # if container is not None:
    #     first_layout = device.findElementByXpath(".//node[@bounds='[0,236][720,344]']")
    #     if first_layout.content()['clickable'] == 'true':
    #         first_layout.click()
    edt_mess = device.findElementByRId('com.zing.zalo:id/chatinput_text')
    edt_mess.sendText('hello world Cừu đen')
    device.findElementByRId('com.zing.zalo:id/new_chat_input_btn_chat_send').click()
    #     else:
    #         print('can find phone')
    # else:
    #     print('Lỗi zalo')
