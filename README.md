# we-jumper
微信跳一跳python脚本

自己写的个自动微信跳一跳的python脚本
运行环境 python3.6.3

使用脚本前置条件
能够执行 adb命令
手机-安卓-打开调试模式-1920*1080分辨率


##原理
利用adb拉取一张截图

根据opencv来比较模板文件的棋子匹配出棋子在屏幕的位置计算出重心点

然后通过边缘检测，来检测出下一个盒子的位置

计算出两个重心点的距离乘以时间系数获得点击屏幕时间

通过adb执行点击屏幕



亲测有效，已经刷了2300分
![image](https://github.com/mejuneyy/we-jumper/blob/master/recoder.jpg?raw=true)
