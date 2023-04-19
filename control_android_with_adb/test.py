""" Created by MrBBS - 4/4/2023 """
# -*-encoding:utf-8-*-

from adb import Device

import time
from pathlib import Path
import subprocess
import os
import shutil
from tqdm import tqdm

class Bot:
    def __init__(self, udid='emulator-5554'):
        self.device = Device(udid)
        self.source_dir = r"E:\DATA\Remove_BG\crawl\xyz"
        self.batch_image = r'E:\Android\images'
        self.output_images = r'E:\Android\Remove\images'
        self.output_masks = r'E:\Android\Remove\masks'
        self.output_photorom = r'E:\Android\OUTPUT\PhotoRoom'

        Path(self.batch_image).mkdir(parents=True, exist_ok=True)
        Path(self.output_images).mkdir(parents=True, exist_ok=True)
        Path(self.output_masks).mkdir(parents=True, exist_ok=True)


    def remove(self):
        self.device.shell(["am", "start", "-n", "com.photoroom.app/com.photoroom.features.home.ui.HomeActivity"])
        if self.device.waitElement(value='com.photoroom.app:id/tab_batch_mode',timeout=10) is not None:
            self.device.findElementByRId('com.photoroom.app:id/tab_batch_mode').click()
        if self.device.waitElement(value='com.photoroom.app:id/home_batch_mode_start',timeout=10) is not None:
            self.device.findElementByRId('com.photoroom.app:id/home_batch_mode_start').click()
        recycler_view = self.device.waitElement(value='com.photoroom.app:id/gallery_recycler_view', timeout=5)
        self.device.swipe(620, 1000, 620, 500, duration=0.5)
        ViewGroups = self.device.waitElements(value="com.photoroom.app:id/image_background", element_count=22,timeout=5)
        
        
        for ViewGroup in ViewGroups:
           ViewGroup.click()
        self.device.waitElement(attr="resource_id",value='com.photoroom.app:id/gallery_picker_select', timeout=5).click()
       
        background_container = self.device.waitElement(
                        value='com.photoroom.app:id/home_create_category_templates_classic_container', timeout=600)
        background_container.findElementByRId('com.photoroom.app:id/photoroom_card_3').click()
        self.device.waitElement("resource_id","com.photoroom.app:id/batch_mode_top_bar_export", has_value='''enabled="true"''',timeout=600).click()
        self.device.waitElement("resource_id","com.photoroom.app:id/share_bottom_sheet_save_to_gallery",timeout=600).click()
        # self.device.touch(200, 1600)


    def add_img_to_gallery(self):
        print(self.device.shell(["adb", "push", f"{self.batch_image}", "/sdcard/Pictures/"]))
        # subprocess.run(f'adb push {self.batch_image} /sdcard/Pictures/')
        
    def reload_gallery(self):
        self.home()
        self.device.shell(["am", "start", "-n", "com.android.gallery3d/.app.GalleryActivity"])
        while True:
            if 'com.android.gallery3d' == self.device.current_package():
                break
        time.sleep(2)
        self.home()

    def remove_gallery(self):
        self.device.shell(["am", "start", "-n", "com.android.gallery3d/.app.GalleryActivity"])
        if self.device.waitElement(attr='class', value='android.widget.ImageButton',timeout=10) is not None:
            self.device.findElementByClass('android.widget.ImageButton').click()
        if self.device.waitElement(attr='text', value='Select album',timeout=10) is not None:
            self.device.findElementByText('Select album').click()
        if self.device.waitElement(value='com.android.gallery3d:id/selection_menu',timeout=10) is not None:
            self.device.findElementByRId('com.android.gallery3d:id/selection_menu').click()
        if self.device.waitElement(attr='text', value='Select all',timeout=10) is not None:
            self.device.findElementByText('Select all').click()
        check = self.device.waitElement(value='com.android.gallery3d:id/selection_menu',timeout=10)
        if check.content()['text'][0] != "0":
            if self.device.waitElement(value='com.android.gallery3d:id/action_delete',timeout=10) is not None:
                self.device.findElementByRId('com.android.gallery3d:id/action_delete').click()
            if self.device.waitElement(value='android:id/button1',timeout=10) is not None:
                self.device.findElementByRId('android:id/button1').click()
            time.sleep(2)
        self.home()

    def home(self):
        self.device.shell(["am", "force-stop", "com.photoroom.app"])
        self.device.shell(["am", "force-stop", "com.android.gallery3d"])
        self.device.shell(["input", "keyevent", "KEYCODE_HOME"])

    def move_file_images(self):
        image_files = [f for f in os.listdir(self.output_photorom) if f.endswith((".png", ".jpg"))]
        if len(image_files) == 22:
            for image_file in image_files:
                path_new_image = os.path.join(self.output_images, image_file)
                path_old_image = os.path.join(self.source_dir, image_file)
                if not os.path.exists(path_old_image):
                    path_old_image = path_old_image.replace('png', 'jpg')

                shutil.move(path_old_image, path_new_image)   
                path_new_mask = os.path.join(self.output_masks, image_file)
                path_old_mask = os.path.join(self.output_photorom, image_file)
                if not os.path.exists(path_old_mask):
                    path_old_mask = path_old_mask.replace('png', 'jpg')
                shutil.move(path_old_mask, path_new_mask)
            print('Thành công!!')
    
    def remove_app_data(self):
        self.home()
        self.device.shell(["am", "start", "-n", "com.photoroom.app/com.photoroom.features.preferences.ui.PreferencesGeneralActivity"])
        if self.device.waitElement(value='com.photoroom.app:id/preferences_general_toolbar',timeout=10) is not None:
            self.device.swipe(500, 900, 500, 500, duration=0.5)
            if self.device.waitElement(attr='text',value='Delete App Data',timeout=10) is not None:
                self.device.findElementByText('Delete App Data').click()
            time.sleep(2)
            self.home()

    def remove_image_batch(self):
        # # print(self.device.shell(["am", "start", "-n", "com.photoroom.app/com.photoroom.features.preferences.ui.PreferencesGeneralActivity"]))
        # # print(self.device.shell(["am", "start", "-n", "com.photoroom.app/com.photoroom.features.home.ui.HomeActivity"]))
        # print(self.device.current_activity())
        # # self.device.shell(["am", "start", "-n", "com.photoroom.app/com.photoroom.features.batch_mode.ui.BatchModeActivity"])
        # # self.device.shell('dumpsys package com.android.gallery3d')
        # # path_cmd = ["adb", "shell", "dumpsys", "package", "com.android.gallery3d"]
        # path_cmd = ["adb", "shell", "pm", "clear", "com.android.gallery3d"]
        # subprocess.run(path_cmd)
        image_files = [f for f in os.listdir(self.source_dir) if f.endswith((".png", ".jpg"))]
        for i in tqdm(range(0, len(image_files), 22)):
            try:    
                # batch = image_files[i:i+22]
                # self.remove_gallery()
                # self.home()
                # shutil.rmtree(self.batch_image)
                # Path(r'E:\Android\OUTPUT\images').mkdir(parents=True, exist_ok=True)
                # Path(r'E:\Android\OUTPUT\PhotoRoom').mkdir(parents=True, exist_ok=True)
                # shutil.rmtree(r'E:\Android\OUTPUT\images')
                # shutil.rmtree(r'E:\Android\OUTPUT\PhotoRoom')
                # Path(self.batch_image).mkdir(parents=True, exist_ok=True)
                # self.remove_app_data()
                # self.reload_gallery()
                # for file_name in batch:
                #     source_file = os.path.join(self.source_dir, file_name)
                #     target_file = os.path.join(self.batch_image, file_name)
                #     shutil.copy(source_file, target_file)
                self.add_img_to_gallery()
                self.reload_gallery()
                # self.home()
                # self.remove()
                # time.sleep(5)
                # self.move_file_images()
                
                self.home()
            except Exception as e:
                print(e)

if __name__ == '__main__':
    bot = Bot()
    bot.remove_image_batch()
