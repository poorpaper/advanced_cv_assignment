#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 检测不到人脸的时候也会输出json，可能会对之后接口造成影响，暂时不改
import json
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *

from openni import openni2
import numpy as np
import cv2
import time

# from openni.utils import OpenNIError

from gui.GUI2 import Ui_MainWindow, ProgressBar
from lib.core.api.facer import FaceAna

if not os.path.exists(os.getcwd() + "\\result\\"):
    os.makedirs(os.getcwd() + "\\result\\")
facer = FaceAna()


class Display:
    def __init__(self, ui, mainWnd):
        self.ui = ui
        self.mainWnd = mainWnd
        self.cap = None
        self.timer_camera = QtCore.QTimer()
        self.playing_states = False
        self.progress_bar = None

        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.count = 0

        self.current_mode = ""
        self.image_or_video_from_path = ""
        self.image_to_path = ""
        self.result_save_path = os.getcwd() + "\\result\\"
        self.per_image_cost = 0.
        self.fps = 0.

        self.depth_stream = None
        self.color_stream = None
        '''
        ui.label.setScaledContents(True)
        ui.label_2.setScaledContents(True)
        ui.label_3.setScaledContents(True)
        '''

        ui.screen1.setAlignment(Qt.AlignCenter)
        ui.screen2.setAlignment(Qt.AlignCenter)
        ui.textLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 信号槽设置
        self.timer_camera.timeout.connect(self.show_camera)
        ui.actionVideo.triggered.connect(self.use_video)
        ui.actionCamera.triggered.connect(self.use_camera)
        # ui.actionKinect.triggered.connect(self.use_kinect)
        ui.actionExit.triggered.connect(self.mainWnd.close)
        ui.actionPictures.triggered.connect(self.use_images)
        ui.pushButton_4.clicked.connect(self.switch)

        ui.pushButton.clicked.connect(self.open_input_dir)
        ui.pushButton_2.clicked.connect(self.open_output_dir)
        ui.pushButton_3.clicked.connect(self.mainWnd.close)

    def reset_state(self, mode, text="Ready to Start"):

        self.current_mode = mode
        self.ui.pushButton_4.setText("Start")
        self.timer_camera.stop()
        self.playing_states = False
        if self.cap is not None:
            self.cap.release()
        self.ui.screen1.clear()
        self.ui.screen2.clear()
        self.ui.textLabel.clear()
        self.ui.screen1.setText(text)
        self.ui.screen2.setText(text)
        self.control_button_disabled()
        self.show_info(before_start=True)

    def create_json(self, landmarks, image_name=None, dpt=None):
        dic = {}
        t = time.time()
        if dpt is not None:  # 说明是Kinect模式
            depth = []
            for face_index in range(landmarks.shape[0]):
                for landmarks_index in range(landmarks[face_index].shape[0]):
                    x_y = landmarks[face_index][landmarks_index]
                    if x_y[0] > 479:
                        x_y[0] = 479
                    if x_y[1] > 639:
                        x_y[1] = 639
                    depth.append(dpt[int(x_y[0]), int(x_y[1])])

            if len(depth) > 0:
                print(len(depth))
                depth = np.array(depth)
                print(depth.shape)
                depth = depth.reshape((landmarks.shape[0], 68, 1))
                landmarks_3d = np.concatenate([landmarks, depth], axis=2)
            else:
                landmarks_3d = np.array([])

            dic['result'] = landmarks_3d.tolist()
            with open(self.result_save_path + str(int(round(t * 1000))) + ".txt", 'w') as json_file:
                json_file.write(json.dumps(dic))

        elif image_name is None:  # camera mode
            dic['result'] = landmarks.tolist()
            with open(self.result_save_path + str(int(round(t * 1000))) + ".txt", 'w') as json_file:
                json_file.write(json.dumps(dic))
        else:
            dic['result'] = landmarks.tolist()
            with open(self.image_to_path + '\\' + image_name + ".txt", 'w') as json_file:
                json_file.write(json.dumps(dic))

    def control_button_disabled(self):
        if self.current_mode == "Camera" or self.current_mode == "Kinect":
            self.ui.pushButton.setDisabled(True)
            self.ui.pushButton_2.setDisabled(False)
        elif self.current_mode == "Video":
            self.ui.pushButton.setDisabled(False)
            self.ui.pushButton_2.setDisabled(False)
        elif self.current_mode == "Images":
            self.ui.pushButton.setDisabled(False)
            self.ui.pushButton_2.setDisabled(False)

    def open_input_dir(self):
        if self.current_mode == "Video":
            self.image_or_video_from_path = os.path.dirname(self.image_or_video_from_path)
        os.system("start %s" % self.image_or_video_from_path)

    def open_output_dir(self):
        if self.current_mode == "Images":
            os.system("start %s" % self.image_to_path)
        else:
            os.system("start %s" % self.result_save_path)

    def switch(self, camid=0):
        if self.current_mode == "":
            return

        if self.current_mode == "Images":
            self.images(self.image_or_video_from_path, self.image_to_path)
        elif not self.timer_camera.isActive():
            if self.current_mode == "Video":
                self.ui.pushButton_4.setText("Pause")
                if self.playing_states:
                    self.timer_camera.start(25)
                else:  # 非手动暂停
                    self.use_camera_or_video(self.image_or_video_from_path)

            elif self.current_mode == "Camera":
                self.ui.pushButton_4.setText("Pause")
                if self.playing_states:
                    self.timer_camera.start(25)
                else:
                    self.use_camera_or_video(camid)

            elif self.current_mode == "Kinect":
                self.ui.pushButton_4.setText("Pause")
                if self.playing_states:
                    self.timer_camera.start(25)
                else:
                    self.use_camera_or_video(camid)
        else:
            self.timer_camera.stop()
            # self.cap.release()
            # self.ui.screen1.clear()
            # self.ui.screen2.clear()
            self.ui.pushButton_4.setText("Start")

    def show_info(self, before_start=True):
        str = ""

        str = " You are using " + self.current_mode + " Mode.\n"
        if self.current_mode == "Images":
             str = str + " Images read from: " + self.image_or_video_from_path + "\n"
             str = str + " Images and result with 68 landmarks will be saved to: " + self.image_to_path + "\n"

        elif self.current_mode == "Kinect":
            str = str + " Attention: Only distance between Kinect and objects in [500, 4500] " + \
                  "can be caught by Kinect." + "\n"

        elif self.current_mode == "Video":
            str = str + " Video read from: " + self.image_or_video_from_path + "\n"

        if self.current_mode != "Images":
            str = str + " Result with 68 landmarks will be saved to: " + self.result_save_path + "\n"

        if not before_start:
            if self.current_mode == "Images":
                str = str + " Done.\n"
            else:
                str = str + " FPS: %.2f" % self.fps + "\n"
                str = str + " One frame cost: %.4f s" % self.per_image_cost

        self.ui.textLabel.setText(str)

    def use_images(self):
        self.image_or_video_from_path = QFileDialog.getExistingDirectory(self.mainWnd,
                                                                         "选择图片所在目录",
                                                                         "./")  # 起始路径

        if self.image_or_video_from_path == "":
            return
        print("\n你选择的文件夹为:")
        print(self.image_or_video_from_path)

        self.image_to_path = QFileDialog.getExistingDirectory(self.mainWnd,
                                                              "选择保存目录",
                                                              "./")

        if self.image_to_path == "":
            return

        self.reset_state("Images", text="No Signal")

    # def use_kinect(self):
    #     self.reset_state("Kinect")

    def use_camera(self):
        self.reset_state("Camera")

    def use_video(self):
        from_path = QtWidgets.QFileDialog.getOpenFileName(self.mainWnd,
                                                          "选择视频所在目录",
                                                          "./")  # 起始路径
        print(from_path[0])
        if not from_path[0].endswith(('.mp4', '.flv', '.avi', '.wmv', '.mkv')):
            return

        self.image_or_video_from_path = from_path[0]
        self.reset_state("Video")

    def use_camera_or_video(self, video_path_or_camid):
        if self.current_mode == "Kinect":
            if not self.timer_camera.isActive():
                try:
                    openni2.initialize()  # can also accept the path of the OpenNI redistribution
                    dev = openni2.Device.open_any()
                    print(dev.get_device_info())

                    self.depth_stream = dev.create_depth_stream()
                    self.color_stream = dev.create_color_stream()

                    self.depth_stream.start()
                    self.color_stream.start()
                except OpenNIError:
                    self.ui.pushButton_4.setText("Start")
                    msg = QtWidgets.QMessageBox.warning(self.mainWnd, u"Warning", u"Kinect连接失败，请查验后重启本程序",
                                                        buttons=QtWidgets.QMessageBox.Ok,
                                                        defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(25)
        else:
            self.cap = cv2.VideoCapture(video_path_or_camid)
            if not self.timer_camera.isActive():
                flag = self.cap.open(video_path_or_camid)
                if flag == False:
                    msg = QtWidgets.QMessageBox.warning(self.mainWnd, u"Warning", u"请检测相机与电脑是否连接正确",
                                                        buttons=QtWidgets.QMessageBox.Ok,
                                                        defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(25)

    def show_camera(self):
        if self.current_mode == "Kinect":
            self.playing_states = True
            if self.playing_states:
                frame = self.depth_stream.read_frame()
                dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
                dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
                dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
                dpt2 *= 255
                dpt = dpt1 + dpt2

                # 显示RGB图像
                cframe = self.color_stream.read_frame()
                cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])

                R = cframe_data[:, :, 0]
                G = cframe_data[:, :, 1]
                B = cframe_data[:, :, 2]
                cframe_data = cv2.merge([R, G, B])

                start = time.time()
                boxes, landmarks, states = facer.run(cframe_data)
                duration = time.time() - start
                if duration == 0:
                    duration = 0.01
                print('one frame cost %f s' % duration)

                self.per_image_cost = duration
                self.fps = 1.0 / duration

                for face_index in range(landmarks.shape[0]):
                    for landmarks_index in range(landmarks[face_index].shape[0]):
                        x_y = landmarks[face_index][landmarks_index]
                        cv2.circle(cframe_data, (int(x_y[0]), int(x_y[1])), 2, (222, 222, 222), -1)

                if self.ui.checkBox.checkState():
                    self.create_json(landmarks, dpt=dpt)

                processed_image = QtGui.QImage(cframe_data.data, cframe_data.shape[1], cframe_data.shape[0],
                                               QtGui.QImage.Format_RGB888)
                temp_pix = QtGui.QPixmap.fromImage(processed_image).scaled(QSize(640, 480),
                                                                           aspectRatioMode=Qt.KeepAspectRatio)
                self.ui.screen1.setPixmap(temp_pix)

                depth_image = QtGui.QImage(dpt.data, dpt.shape[1], dpt.shape[0], QtGui.QImage.Format_ARGB32)
                temp_pix = QtGui.QPixmap.fromImage(depth_image).scaled(QSize(640, 480),
                                                                       aspectRatioMode=Qt.KeepAspectRatio)
                self.ui.screen2.setPixmap(temp_pix)

                self.show_info(before_start=False)

            else:
                self.timer_camera.stop()
                self.ui.pushButton_4.setText("Start")

        else:
            self.playing_states, image = self.cap.read()
            if self.playing_states:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                '''
                scale_x = image.shape[1] / 480
                scale_y = image.shape[0] / 360
                scale = min(scale_x, scale_y)
                image = cv2.resize(image, None, fx=scale, fy=scale)
                '''
                show = image.copy()
                start = time.time()

                boxes, landmarks, states = facer.run(image)
                duration = time.time() - start
                if duration == 0:
                    duration = 0.01
                print('one frame cost %f s' % duration)

                self.per_image_cost = duration
                self.fps = 1.0 / duration

                for face_index in range(landmarks.shape[0]):

                    for landmarks_index in range(landmarks[face_index].shape[0]):
                        x_y = landmarks[face_index][landmarks_index]
                        cv2.circle(show, (int(x_y[0]), int(x_y[1])), 2, (222, 222, 222), -1)

                if self.ui.checkBox.checkState():
                    self.create_json(landmarks)

                processed_image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
                temp_pix = QtGui.QPixmap.fromImage(processed_image).scaled(QSize(640, 480),
                                                                           aspectRatioMode=Qt.KeepAspectRatio)
                self.ui.screen2.setPixmap(temp_pix)

                origin_image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
                temp_pix = QtGui.QPixmap.fromImage(origin_image).scaled(QSize(640, 480),
                                                                        aspectRatioMode=Qt.KeepAspectRatio)
                self.ui.screen1.setPixmap(temp_pix)
                self.show_info(before_start=False)

            else:
                self.timer_camera.stop()
                self.ui.pushButton_4.setText("Start")

    def images(self, from_path, dst_path):
        image_list = os.listdir(from_path)
        image_list = [x for x in image_list if x.endswith(('.jpg', '.png'))]
        image_list.sort()

        file_num = len(image_list)
        self.progress_bar = ProgressBar(0, file_num)

        index = 0
        for image_name in image_list:
            index += 1
            #image = cv2.imread(os.path.join(from_path, image_name))
            image = cv2.imdecode(np.fromfile(os.path.join(from_path, image_name), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            print(os.path.join(from_path, image_name))
            # cv2.imshow("capture", image)
            img_show = image.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            start = time.time()
            boxes, landmarks, states = facer.run(image)

            ###no track
            facer.reset()

            duration = time.time() - start
            print('one image cost %f s' % duration)

            for face_index in range(landmarks.shape[0]):

                for landmarks_index in range(landmarks[face_index].shape[0]):
                    x_y = landmarks[face_index][landmarks_index]
                    cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 1,
                               (222, 222, 222), -1)

            #cv2.imwrite(os.path.join(dst_path, image_name), img_show)
            img_write = cv2.imencode(".jpg", img_show)[1].tofile(os.path.join(dst_path, image_name))

            self.progress_bar.changeValue(index)
            QApplication.processEvents()
            if self.ui.checkBox.checkState():
                self.create_json(landmarks, image_name=image_name)
            '''
            if args.mask:
                cv2.namedWindow("masked", 0)
                cv2.imshow("masked", image*pattern)


            key = cv2.waitKey(0)
            if key == ord('q'):
                return
            '''
        self.progress_bar.close()
        self.show_info(before_start=False)

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            # self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    mainWnd = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWnd)
    display = Display(ui, mainWnd)
    mainWnd.show()
    sys.exit(App.exec_())
