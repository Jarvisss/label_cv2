import cv2
import os
import numpy as np
import copy
import json

screen_w = 1920
screen_h = 1080

drawing=False
mode=False
ix,iy=-1,-1
nearest_pt = -1
nearest_pt_temp = [0,0]


def dist(sx,sy,tx,ty):
    return (sx-tx)**2 + (sy-ty)**2

def nearest_point(x,y,j2d):
    min_dist = 1000000
    nearest = 0
    for i in range(0,len(j2d)):
        distance = dist(x,y,j2d[i][0],j2d[i][1])
        if min_dist > distance:
            min_dist = distance
            nearest = i

    return nearest

def on_Mouse(event, x, y, flags, param):
    global ix, iy, drawing, mode, nearest_pt, nearest_pt_temp
    img_mat = param[0]
    oneJ2d = param[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        print('EVENT_LBUTTONDOWN')
        nearest_pt = nearest_point(x,y,oneJ2d)
        print("nearest: %d"%nearest_pt)
        ix = x
        iy = y
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        print('EVENT_MOUSEMOVE')
        if drawing == True:
            print("nearest: %d, ixy:(%d, %d), xy:(%d, %d)" % (nearest_pt,ix,iy,x,y))
            oneJ2d[nearest_pt][0] = oneJ2d[nearest_pt][0] + (x - ix)
            oneJ2d[nearest_pt][1] = oneJ2d[nearest_pt][1] + (y - iy)
            ix = x
            iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        print('EVENT_LBUTTONUP')

        drawing = False

    pass

def labelOneImg(img, oneJ2d, win_name):
    img_copy = copy.deepcopy(img)
    cv2.setMouseCallback(win_name, on_Mouse, param=[img, oneJ2d])
    while True:
        img = copy.deepcopy(img_copy)

        for i in range(0, len(oneJ2d)):
            cv2.putText(img, str(i), (int(oneJ2d[i][0]), int(oneJ2d[i][1])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
            cv2.circle(img, (int(oneJ2d[i][0]), int(oneJ2d[i][1])), 1, (0, 0, 255), -1)
        cv2.imshow(win_name, img)

        k = cv2.waitKey(1)

        if k == ord(' '):
            print('press space')
            break
    return oneJ2d



def labelImg(img_dir,json_path,win_name):
    imgs = os.listdir(img_dir)


    cv2.namedWindow(win_name)
    save_freq = 100
    with open(json_path, 'r') as fp:
        allJ2d = json.load(fp)
    for i in range(0,len(imgs)):

        cv2.setWindowTitle(win_name, title='Frame: %d' % i)
        new_j2d = labelOneImg(cv2.imread(os.path.join(img_dir,imgs[i])),allJ2d[i], win_name)
        allJ2d[i] = new_j2d
        if i%save_freq == save_freq-1:
            print('save for frame %d' % i)
            with open(json_path, 'w') as fp:
                json.dump(allJ2d, fp)
        pass





if __name__ == '__main__':
    img_dir = 'G:/Neural_rendering/video_frame/C0033_540_540_12032'
    json_path = 'G:/Neural_rendering/FK/imgui_gltf_viewer/models/output_C0033_2d_copy.json'
    labelImg(img_dir=img_dir,json_path=json_path, win_name='img_show')