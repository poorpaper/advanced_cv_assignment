# advanced_cv_assignment

advanced computer vision assignment
ID:2020244123

## 主要工作

使用了基于ShuffleNetV2主干网络的简化后的dsfd作为人脸检测模型，然后使用ShuffleNetV2直接作为人脸关键点定位模型，并使用PyQt作为GUI，完成整个项目。

## requirement

+ python 3.6

+ PyQt5

+ tensorflow-gpu==2.0.0

+ tensorpack==0.9.9

+ opencv_python==3.4.3.18

+ numpy==1.14.0

+ easydict==1.7

+ matplotlib==3.0.2

+ imageio==2.4.1

## 运行

直接运行facial_landmark内的video.py即可启动GUI，允许的输入包括：摄像头，图片，视频。
模型已经上传到仓库中，直接下载即可
可以实时查看每一帧运行用时，选择是否输出每一帧的人脸关键点等。

## 数据集及训练

人脸检测（mini-DSFD）：
  1. 下载WIDER FACE数据集 http://shuoyang1213.me/WIDERFACE/
     然后解压WIDER_train, WIDER_val 和 wider_face_split 到 ./WIDER, 接着运行
     ```python prepare_wider_data.py```

  2. 运行 ```python train.py```来训练
  
人脸关键点定位（shufflnet_landmark）：
  1. 下载300W数据集 https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/
     下载300VW数据集 https://ibug.doc.ic.ac.uk/resources/300-VW/
     其中300VW需要把其中的每个视频分割为一张一张的图片以供训练
     然后解压下载好的数据集 到 ./300W, 接着运行cut.sh文件以完成300VW的分割
  
  2. 运行 ```python make_json.py```

  3. 运行 ```python train.py```来训练


