YOLO 이미지 Detection + Cropping 사용법

1. Google Drive(https://drive.google.com/drive/u/0/folders/1aUW2jgaStVM5mq7X4Z8DS_NtvTjfrjCZ)에서 yolov3.weights를 다운받습니다.
2. yolov3.weights 파일을 yolo-coco 폴더에 넣어주세요.

3. cmd(Terminal)을 실행합니다.
4. yolo.py가 있는 폴더로 이동합니다. (cd 명령어 사용)
5. 실행 명령어는 다음과 같습니다.
"python yolo.py --image images/soccer.jpg --yolo yolo-coco"

6. 크롭된 이미지는 yolo.py가 있는 폴더에 저장됩니다.