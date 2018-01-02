#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# athor cutewoo)yang
#开发环境 python 3.6.3

import cv2
import numpy as np
import os
import subprocess
import time
import sys


#获取应该跳的距离
def get_distance(res_screen):
	res_chess = cv2.imread("./misc/chess.png", 0)

	res_screen_display = res_screen.copy()

	w, h = res_chess.shape[::-1]
	page_w, page_h = res_screen.shape[::-1]

	check_result = cv2.matchTemplate(res_chess, res_screen, cv2.TM_CCOEFF_NORMED)
	min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(check_result)

	#匹配棋子的结果输出
	#cv2.rectangle(res_screen_display, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,0,255), 3)
	#cv2.imwrite('res.png', res_screen_display)

	#棋子的重心坐标
	chess_center_gravity_x =  int(max_loc[0] + w/2)
	chess_center_gravity_y = int(max_loc[1] + h - 20)

	#重心标点
	#cv2.circle(res_screen_display, (chess_center_gravity_x, chess_center_gravity_y), 3, (255,255,255))
	#cv2.imwrite('res.png', res_screen_display)

	#边缘检测
	res_screen_display = cv2.GaussianBlur(res_screen_display,(5,5),0)  
	canny = cv2.Canny(res_screen_display, 1, 10) 
	#cv2.imwrite('res.png', canny)

	# 消去小跳棋轮廓对边缘检测结果的干扰 
	# 原理，抹去棋子的图案
	for k in range(max_loc[1]-10, max_loc[1] + 189):
	            for b in range(max_loc[0]-10, max_loc[0] + 100):
	                canny[k][b] = 0
	#cv2.imwrite('res.png', canny)


	# 计算物块上沿的坐标 从屏幕的1/3处开始扫描，以免扫到了记分器
	cal_h = int(page_h * 1 / 3)
	target_y = np.nonzero([max(row) for row in canny[cal_h:]])[0][0] + cal_h

	target_x = int(np.mean(np.nonzero(canny[target_y])))
	target_y += 50  # 偏移，需要设置得小一点，因为游戏到后面会出现非常小的物块

	#canny = cv2.circle(canny, (target_x, target_y), 10, 255)
	#cv2.imwrite('res.png', canny)

	#计算两个圆点之间的距离 直角三角形求斜边
	distance = (target_x - chess_center_gravity_x) ** 2 + (target_y - chess_center_gravity_y) ** 2
	distance = distance ** 0.5
	return distance

#获取一张截图
def pull_screenshot():
	process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
	screenshot = process.stdout.read()
	if sys.platform == 'win32':
		screenshot = screenshot.replace(b'\r\n', b'\n')
	f = open('./misc/default_screen.png', 'wb')
	f.write(screenshot)
	f.close()
	return cv2.imread("./misc/default_screen.png", 0)

#起跳
def jump(distance):
    press_time = distance * 1.35
    press_time = max(press_time, 200)   # 设置 200 ms 是最小的按压时间
    press_time = int(press_time)
    cmd = 'adb shell input swipe 320 410 320 410 {duration}'.format(duration=press_time)
    os.system(cmd)

while True:
	#获得截图
	im = pull_screenshot()
	#获取距离
	distance = get_distance(im)
	#起跳
	jump(distance)
	#延迟三秒
	time.sleep(3)