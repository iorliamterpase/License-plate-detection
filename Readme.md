THIS PROJECTS USES YOLOV8 ARCHITECTURE TO TRAIN AND DETECT CAR LICENSE PLATES



## clone this repository and cd into it

## create and activate a virtual environment

```
python -m venv yolo-v8
.\yolo-v8\Scripts\activate
```

## pip install -r requirements.txt
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run inference on a video 
```
python license.py --weights ./weights/best.pt --source ./path/to/video.mp4
```






