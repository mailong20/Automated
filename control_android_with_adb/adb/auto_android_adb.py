""" Created by MrBBS """
# 6/23/2022
# -*-encoding:utf-8-*-
import base64
import re
import tempfile
import time
import xml.etree.cElementTree as ET

from adbutils import adb


class Element(object):
    def __init__(self, tree, device):
        if isinstance(tree, str):
            self.tree = ET.fromstring(tree)  # ET.parse(tree)
        else:
            self.tree = tree
        self.pattern = re.compile(r"\d+")
        self.type_search = {
            0: 'index',
            1: 'resource-id',
            2: 'text',
            3: 'class',
            4: 'xpath'
        }
        self.device = device

    def toString(self):
        return ET.tostring(self.tree)

    def content(self):
        return self.tree.attrib

    def __element(self, attr, value):
        try:
            if attr =='xpath':
                element = self.tree.find(value)
            else:
                element = self.tree.find(f".//node[@{attr}='{value}']")
            element = ET.tostring(element)
            element = ET.fromstring(element)
            if element is not None:
                return Element(element, self.device)
        except:
            pass
        return None
    
    def __elements(self, attr, value):
        try:
            if attr =='xpath':
                elements = self.tree.findall(value)
            else:
                elements = self.tree.findall(f".//*[@{attr}='{value}']")
           
            elements = [ET.tostring(element) for element in elements]
            elements = [ET.fromstring(element)for element in elements]
            if elements is not None:
                return [Element(element, self.device) for element in elements]
        except:
            pass
        return None

    def findElementByIndex(self, index):
        """
        Find by the index of the element
        findElementByIndex("0")
        """
        return self.__element(self.type_search[0], str(index))

    def findElementByRId(self, resource_id):
        """
        Find by the resource-id of the element
        findElementByRId("com.android.deskclock:id/imageview")
        """
        return self.__element(self.type_search[1], resource_id)
    
    def findElementsByRId(self, resource_id):
        """
        Find by the resource-id of the element
        findElementByRId("com.android.deskclock:id/imageview")
        """
        return self.__elements(self.type_search[1], resource_id)

    def findElementByText(self, text):
        """
        Find by the text of the element
        findElementByText("Cừu Đen")
        """
        return self.__element(self.type_search[2], text)

    def findElementByClass(self, class_name):
        """
        Find by the class of the element
        findElementByClass("android.widget.TextView")
        """
        return self.__element(self.type_search[3], class_name)
    
    def findElementsByClass(self, class_name):
        """
        Find by the class of the element
        findElementByClass("android.widget.TextView")
        """
        return self.__elements(self.type_search[3], class_name)

    def findElementByXpath(self, xpath):
        try:
            element = self.tree.find(xpath)
            element = ET.tostring(element)
            element = ET.fromstring(element)
            if element is not None:
                return Element(element, self.device)
        except:
            pass
        return None
    
    def findElementsByXpath(self, xpath):
        return self.__elements(self.type_search[4], xpath)

    def getPoint(self):
        """
        Get center point of current element


        :return: x, y
        """
        coord = self.tree.attrib["bounds"][1:-1].split('][')
        x1, y1 = map(int, coord[0].split(','))
        x2, y2 = map(int, coord[1].split(','))
        x = x1 + (x2 - x1) // 2
        y = y1 + (y2 - y1) // 2
        return int(x), int(y)

    def click(self):
        x, y = self.getPoint()
        self.device.click(x+5, y+5)

    def sendText(self, text):
        self.click()
        self.device.shell("am broadcast -a ADB_INPUT_B64 --es msg %s" % str(base64.b64encode(text.encode('utf-8')))[1:])

    def swipe(self, sx, sy, ex, ey, duration: float = 1.0):
        x1, y1, x2, y2 = map(str, [sx, sy, ex, ey])
        return self.shell(
            ['input', 'swipe', x1, y1, x2, y2,
                str(int(duration * 1000))])
        


class Device:
    def __init__(self, serial):
        self.serial = serial
        self.temp = tempfile.gettempdir()
        self.device = adb.device(serial=self.serial)
        if not self.device.package_info('com.android.adbkeyboard'):
            self.device.install('adb/ADBKeyboard.apk')
        if 'com.android.adbkeyboard/.AdbIME' != self.__command('settings get secure default_input_method'):
            self.__command('ime set com.android.adbkeyboard/.AdbIME')

    def __command(self, cmd):
        return self.device.shell(cmd)

    def shell(self, cmd):
        return self.device.shell(cmd)

    def __uidump(self):
        ui = self.device.dump_hierarchy()
        return ui

    def current_activity(self):
        return self.device.app_current().activity

    def current_package(self):
        return self.device.app_current().package

    def findElementByIndex(self, index):
        """
        Find by the index of the element
        findElementByIndex("0")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementByIndex(index)

    def findElementByRId(self, resource_id):
        """
        Find by the resource-id of the element
        findElementByRId("com.android.deskclock:id/imageview")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementByRId(resource_id)
    

    def findElementsByRId(self, resource_id):
        """
        Find by the resource-id of the element
        findElementByRId("com.android.deskclock:id/imageview")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementsByRId(resource_id)
    

    def findElementByText(self, text):
        """
        Find by the text of the element
        findElementByText("Cừu Đen")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementByText(text)

    def findElementByClass(self, class_name):
        """
        Find by the class of the element
        findElementByClass("android.widget.TextView")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementByClass(class_name)
    

    def findElementsByClass(self, class_name):
        """
        Find by the class of the element
        findElementByClass("android.widget.TextView")
        """
        ui = self.__uidump()
        return Element(ui, self.device).findElementsByClass(class_name)


    def findElementByXpath(self, xpath):
        ui = self.__uidump()
        return Element(ui, self.device).findElementByXpath(xpath)
    
    def findElementsByXpath(self, xpath):
        ui = self.__uidump()
        return Element(ui, self.device).findElementsByXpath(xpath)

    def waitElement(self, attr='resource_id', value=None, has_value=None, timeout=1):
        """
        wait for element appear
        waitElement("class", "android.widget.TextView", 10)
        :param attr: resource_id | text | class
        :param timeout: second
        """
        timeout += time.time()
        if attr not in ['resource_id', 'text', 'class', 'xpath']:
            raise ValueError('attr must be resource_id | text | class')
        if value is None:
            raise ValueError('Value must not none')
        element = None
        while True:
            if time.time() > timeout:
                break
            if attr == 'resource_id':
                element = self.findElementByRId(value)
            elif attr == 'text':
                element = self.findElementByText(value)
            elif attr == 'class':
                element = self.findElementByClass(value)
            elif attr == 'xpath':
                element = self.findElementByXpath(value)
            if element is not None and has_value is None:
                break
            if element is not None and has_value is not None and has_value in element.toString().decode('utf-8'):
                break
        # print(element)
        return element
    
  


    def waitElements(self, attr='resource_id', value=None, element_count=None,timeout=1):
        """
        wait for element appear
        waitElement("class", "android.widget.TextView", 10)
        :param attr: resource_id | text | class
        :param timeout: second
        """
        timeout += time.time()
        if attr not in ['resource_id', 'text', 'class', 'xpath']:
            raise ValueError('attr must be resource_id | text | class')
        if value is None:
            raise ValueError('Value must not none')
        elements = None
        while True:
            if time.time() > timeout:
                break
            if attr == 'resource_id':
                elements = self.findElementsByRId(value)
            # elif attr == 'text':
            #     element = self.findElementByText(value)
            elif attr == 'class':
                elements = self.findElementsByClass(value)
            elif attr == 'xpath':
                elements = self.findElementsByXpath(value)
            if not element_count  and len(elements) == element_count:
                break
        return elements
    


    def touch(self, dx, dy):
        """
        Touch event
        usage: touch(500, 500)
        """
        self.device.click(dx, dy)

    def swipe(self, sx, sy, ex, ey, duration):
        self.device.swipe(sx, sy, ex, ey, duration)
        

