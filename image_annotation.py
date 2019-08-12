import glob
import argparse
import cv2
import numpy as np
import re

debug = True

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="inform directory path with images to be annotated.")
parser.add_argument("--save", "-s", help="inform directory paht in which the annotation must be saved.")
parser.add_argument("--resume", "-c", help="resume from a specific frame number.")

args = parser.parse_args()

if(args.path != None):
    path = args.path
else:
    path = "."

if(args.save != None):
    savepath = args.save
else:
    savepath = "."

if(args.resume != None):
    frame_resume = args.resume
else:
    frame_resume = None

if(debug):
    print("path", path)
    print("savepath", savepath)

# ipdb.set_trace()
if(frame_resume == None):
    try:
        last_annotation = open(savepath+"/annotation.log","r")
        frame_resume = int(re.findall(r'\d+',last_annotation.readlines()[0])[0])
        print("Last annotation was on frame ", frame_resume)
    except:
        last_annotation = open(savepath+"/annotation.log", "w")
        last_annotation.close()
        frame_resume = -1
        if(debug):
            print("openned new annotation.log")

def update_log(index):
    last_annotation = open(savepath+"/annotation.log", "w")
    last_annotation.write(index)
    last_annotation.close()
    if(debug):
        print("log updated")

global refPt, copy, first

def polygon_select(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        cv2.circle(copy,(x,y),3,(0,255,0))
        cv2.imshow("image",copy)
        
        refPt.append((x,y))
        print(refPt)


cv2.namedWindow("image")
cv2.setMouseCallback("image", polygon_select)

for frame in sorted(glob.iglob(path+"/*.jpg")):
    frameid = int(re.findall(r'\d+',frame[-10:])[0])
    if (frameid <= frame_resume):
        print("Frame ", frameid, " already annotated.")
        pass
    else:
        print(frameid)
        img = cv2.imread(frame)
        copy = img.copy()
        
        refPt = []
        first = False

        while(True):
            cv2.imshow("image",copy)
            key = cv2.waitKey(0)

            if (key == ord('r')):
                refPt = []
                copy = img.copy()
                cv2.imshow("image",copy)
                print("Reset points.")
            
            if (key == ord('c')):
                mask = np.zeros(img.shape[:-1], dtype = np.uint8)
                cv2.fillPoly(mask, np.array([refPt], dtype=np.int32), 255)
                cv2.imshow("mask", mask)

                frameid = re.findall(r'\d+',frame[-10:])[0]
                
                cv2.imwrite(savepath+"/annotation"+frameid+".jpg",mask)
                update_log(frameid)
                break
                print("Save and continue...")
            
            if (key == ord('q')):
                exit()

