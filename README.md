# StarRailStationBackpackRecognitionUpload

## 注意

工具需要在 **1920*1080全屏幕** 分辨率下使用，此外的分辨率均有概率导致工具识别出错

## 介绍

星穹铁道[StarRailStation](https://starrailstation.com/cn)养成计算页面背包材料识别上传工具



## 使用说明

目前只做了chrome、edge的适配

在工具**Resources\confing.ini**中为***browser***的**browser**设置使用的浏览器

### Chrome使用方法

需要将***Chrome***添加到环境变量中

在工具**Resources\confing.ini**中为***chrome***的***userDataDir***添加目录

例如 ***userDataDir = C:\Users\username\AppData\Local\Google\Chrome\User Data***

> 注：
>
> 1. 此目录必须设置，否则工具无法连接至浏览器
> 2. 示例目录是浏览器默认的用户数据存储位置，若使用此路径，请确保所有该浏览器进程均关闭，否则浏览器无法被控制
> 3. 此目录只是作为浏览器用户数据存放位置，可以自己新建一个文件夹给脚本用，避免污染自己的浏览器记录

最后双击**StarRailStationBackpackRecognitionUpload.exe**即可运行工具

### Edge使用方法

使用方法和***Chrome***类似

需要将***Edge***添加到环境变量中

在工具**Resources\confing.ini**中为***chrome***的***userDataDir***添加目录

例如 ***userDataDir = C:\Users\username\AppData\Local\Microsoft\Edge\User Data***

最后双击**StarRailStationBackpackRecognitionUpload.exe**即可运行工具



## 致谢

#### 开源库

- 图像识别库：[opencv](https://github.com/opencv/opencv.git)

- 文字识别库：[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)

