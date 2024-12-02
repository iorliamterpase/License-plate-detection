THIS PROJECTS USES YOLOV8 ARCHITECTURE TO TRAIN AND DETECT CAR LICENSE PLATES



clone this repository and cd into it

download trained weights here: https://drive.google.com/file/d/1fISGdH9iKrcB7mF0D_rZzBrgFzBKOAlR/view?usp=drive_link

move downloaded weights into your work folder

create and activate a virtual environment

python -m venv yolo-v8

pip install -r requirements.txt

download inference video using this link: https://videos.pexels.com/video-files/7741449/7741449-sd_640_360_24fps.mp4

Run inference on a video 

python license.py --weights ./weights/best.pt --source ./path/to/video.mp4

Run inference on image

python license.py --weights ./weights/best.pt --source ./images.jpeg/image.jpg





