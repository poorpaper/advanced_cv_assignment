
import cv2
import time
import numpy as np
import os
import argparse

from lib.core.api.facer import FaceAna
from lib.core.headpose.pose import get_head_pose, line_pairs


facer = FaceAna()

def test():
    from gui.GUI import Ui_MainWindow
    image_list = os.listdir("C:/Users/sdfgh/Desktop/testImages/")
    image_list.sort()
    Ui_MainWindow.origin_image = image_list[2]
    Ui_MainWindow.processed_image = image_list[3]
    Ui_MainWindow.depth_image = image_list[4]
    print(image_list[1])


def video(video_path_or_cam):
    vide_capture=cv2.VideoCapture(video_path_or_cam)

    while 1:

        ret, image = vide_capture.read()

        pattern = np.zeros_like(image)

        img_show = image.copy()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        star=time.time()
        boxes, landmarks, states = facer.run(image)

        duration=time.time()-star
        print('one iamge cost %f s'%(duration))

        for face_index in range(landmarks.shape[0]):

            #######head pose need develop
            #reprojectdst, euler_angle=get_head_pose(landmarks[face_index],img_show)
            '''
            if args.mask:
                face_bbox_keypoints = np.concatenate(
                    (landmarks[face_index][:17, :], np.flip(landmarks[face_index][17:27, :], axis=0)), axis=0)

                pattern = cv2.fillPoly(pattern, [face_bbox_keypoints.astype(np.int)], (1., 1., 1.))
            '''

            # for start, end in line_pairs:
            #     cv2.line(img_show, reprojectdst[start], reprojectdst[end], (0, 0, 255),2)
            #
            # cv2.putText(img_show, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)
            # cv2.putText(img_show, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)
            # cv2.putText(img_show, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)

            for landmarks_index in range(landmarks[face_index].shape[0]):

                x_y = landmarks[face_index][landmarks_index]
                cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 1,
                           (222, 222, 222), -1)


        #cv2.namedWindow("capture", 0)
        #cv2.imshow("capture", img_show)

        '''
        if args.mask:
            cv2.namedWindow("masked", 0)
            cv2.imshow("masked", image*pattern)
        '''
        #key=cv2.waitKey(1)
        #if key==ord('q'):
        #    return


def images(image_dir):
    from gui.GUI import Ui_MainWindow

    image_list = os.listdir(image_dir)
    image_list = [x for x in image_list if 'jpg' in x or 'png' in x]
    image_list.sort()

    for image_name in image_list:

        image = cv2.imread(os.path.join(image_dir, image_name))
        print(os.path.join(image_dir, image_name))
        #pattern = np.zeros_like(image)
        cv2.imshow("capture", image)
        img_show = image.copy()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        star = time.time()
        boxes, landmarks, states = facer.run(image)

        ###no track
        facer.reset()

        duration=time.time()-star
        print('one image cost %f s'%(duration))

        for face_index in range(landmarks.shape[0]):

            #######head pose
            #reprojectdst, euler_angle=get_head_pose(landmarks[face_index],img_show)
            '''
            if args.mask:
                face_bbox_keypoints = np.concatenate(
                    (landmarks[face_index][:17, :], np.flip(landmarks[face_index][17:27, :], axis=0)), axis=0)

                pattern = cv2.fillPoly(pattern, [face_bbox_keypoints.astype(np.int)], (1., 1., 1.))
            '''

            # for start, end in line_pairs:
            #     cv2.line(img_show, reprojectdst[start], reprojectdst[end], (0, 0, 255),2)
            #
            # cv2.putText(img_show, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)
            # cv2.putText(img_show, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)
            # cv2.putText(img_show, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.75, (0, 0, 0), thickness=2)

            for landmarks_index in range(landmarks[face_index].shape[0]):

                x_y = landmarks[face_index][landmarks_index]
                cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 1,
                           (222, 222, 222), -1)


        cv2.namedWindow("capture", 0)
        cv2.imshow("capture", img_show)
        cv2.imwrite(os.path.join(Ui_MainWindow.dst_image_path, image_name), img_show)

        '''
        if args.mask:
            cv2.namedWindow("masked", 0)
            cv2.imshow("masked", image*pattern)
        '''

        key = cv2.waitKey(0)
        if key == ord('q'):
            return


def build_argparse():
    parser = argparse.ArgumentParser(description='Start train.')
    parser.add_argument('--video', dest='video', type=str, default=None, \
                        help='the camera id (default: 0)')
    parser.add_argument('--cam_id', dest='cam_id', type=int, default=0, \
                        help='the camera to use')
    parser.add_argument('--img_dir', dest='img_dir', type=str, default=None, \
                        help='the images dir to use')

    parser.add_argument('--mask', dest='mask', type=bool, default=False, \
                        help='mask the face or not')
    args = parser.parse_args()
    return  args

'''
if __name__=='__main__':




    args=build_argparse()


    if args.img_dir is not None:
        images(args.img_dir)

    elif args.video is not None:
        video(args.video)
    else:
        video(args.cam_id)
'''
