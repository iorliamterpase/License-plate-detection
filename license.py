import cv2
from ultralytics import YOLO
import math
import paddleocr
from paddleocr import PaddleOCR
import numpy as np
import re
import os
from datetime import datetime
import json
import argparse

parser = argparse.ArgumentParser(description='Run license plate detection')
parser.add_argument('-w', '--weight', type=str, default="best.pt", help='Path to weights', required=True)
parser.add_argument('-s', '--source', type=str, default="test_video.mp4", help='Source path', required=True)
args = parser.parse_args()


os.environ["KMP_DUPLICATE_LIB_OK"]= "True"


# Replace 'path_to_video.mp4' with the actual path to your video file
cap = cv2.VideoCapture(args.source)

#initialize yolo model
model= YOLO(args.weight)

#initialize frame count
count=0

className=['license']
#initialize paddleocr 
ocr= PaddleOCR(use_angle_cls=True, use_gpu=False)


def paddleocr(frame,x1,y1,x2,y2):
    frame[y1:y2,x1:x2]
    result= ocr.ocr(frame,det=False,rec=True,cls=False)
    text=""
    for r in result:
        scores=r[0][1]
        if np.isnan(scores):
            scores=0
        else:
             scores=int(scores *100)
        if scores>60:
            text=r[0][0]
    pattern= re.compile('[/W]')
    text=pattern.sub('',text)
    text=text.replace("???"," ")
    text=text.replace("O","0")
    return str(text)

# def save_json(interval_filepath, license_nums, startTime, endTime):
#     #generate individual json_file for each 20 seconds
#     interval_data = {
#         "StartTime":startTime.isoformat(),
#         "endTime":endTime.isoformat(),
#         "license_numbers":license_nums
#         }

#     with open (interval_filepath,'w') as f:
#         json.dump(interval_data,f,indent=2)

    

directory = "json"
interval_filepath = os.path.join(directory, f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")

# Ensure the directory exists
os.makedirs(directory, exist_ok=True)



# # Json file
# json_filepath="json/LicensePlateDetection.json"
# if os.path.exists(cummulative_filepath):
#     with open(cummulative_filepath,'r')as f:
#         existing_data=json.load(f)
# else:
#     existing_data=[]

# existing_data.append("interval_data")

# #add new interval data to cummulative data

# with open (cummulative_filepath,'w') as f:
#     json.dump(existing_data,f,indent=2)



startTime=datetime.now()
license_nums=set()
while True:
    ret, frame = cap.read()
    if ret:
        currentTime=datetime.now()
        count += 1
        print(f"frame Number:{count}")
        result=model.predict(frame,conf=0.45)
        for r in result:
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2= int(x1),int(y1),int(x2),int(y2)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
                classNameInt=int(box.cls[0])
                clsname= className[classNameInt]
                conf= math.ceil(box.conf[0]*100/100)
                #label= f'{className}:{conf}'
                label=paddleocr(frame,x1,y1,x2,y2)
                if label:
                    license_nums.add(label)
                textsize=cv2.getTextSize(label, 0, fontScale=0.5,thickness=2)[0]
                c2=x1 + textsize[0],y1 - textsize[1] -3
                # cv2.rectangle(frame, (x1, y1), c2, (255-1, 0, 0), thickness=2)
                cv2.putText(frame, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, lineType=cv2.LINE_AA)


        endTime=currentTime 
    # if (currentTime - startTime).seconds >= 20:
    cv2.imshow("Video", frame)
    # save_json(interval_filepath, license_nums, startTime, endTime)
    startTime=currentTime
    # Press 'q' to quit the video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else:
        continue

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()


