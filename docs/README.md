# 4조 DeepCycle 보고서

## 서론

### 문제 인식

1. 우리나라 **재활용률**의 허와 실
    1. 우리나라 재활용률은 60%로 OECD 국가 중 2위를 차지하고 있습니다.
    1. 쓰레기 처리 과정은 수집-선별-처리 3단계를 거칩니다.
    1. 상식적으로 '재활용률'이라 함은 3단계를 모두 거치는 재활용 쓰레기의 비율이라고 생각하기 쉽습니다.
    1. 그러나 우리나라는 선별장까지 가는 비율을 '재활용률'로 정의합니다.
    1. 선별장에서 실제 처리까지 이루어지는 재활용 쓰레기의 비율은 공공기관 통계상 60%입니다.
    1. 쓰레기 처리는 대부분 민간업체가 수행합니다. 따라서 통계에 잡히지 않는 데이터를 고려한다면 실제 처리 비율은 60%미만일 것입니다.
    1. 따라서 3단계를 모두 거치는 재활용 쓰레기의 비율은 36%미만입니다.

1. **쓰레기의 종류**와 **분리배출 요령**을 명확하게 알기 어려움
    1. 초코송이 포장상자, 프링글스 - 일반쓰레기 / 양갱 포장상자 - 종이
    1. 위의 예시처럼 '종이'로 보이는 쓰레기들은 사실 일반쓰레기였습니다.
    1. 같은 모양의 쓰레기라도 다양한 재질로 이루어져 있기 때문에 어디에 버려야할 지 혼동하기 쉽습니다.
    1. 종류를 구분짓는데 성공하더라도 올바른으로 방법 배출하지 않으면 추가 선별작업을 거쳐야 합니다.
    1. 따라서 쓰레기의 종류를 정확하게 구분한 후 올바른 방법으로 재활용 쓰레기를 배출해야 합니다.

## 본론

버려지는 쓰레기 중 재활용 가치가 큰 캔, 페트, 병을 이미지 처리 기술만으로 구별하고자 합니다.

### 데이터셋 구성

1. 크롤링
    1. 국내 주요 포털사이트(구글, 네이버, 다음)에서 총 60개의 키워드로 캔, 페트, 병 이미지 35,000장 수집
    1. html, gif를 제외한 jpg, jpeg, png파일만 수집
    1. 검색어와 유관한 이미지만 필터링 => 13,468장 수집

1. 데이터 전처리
    1. jpg, jpeg, png를 3채널로 통일
    1. alpha channel을 제외하고 RGB로 통일

1. Annotation
    1. [VGG Annotation](http://www.robots.ox.ac.uk/~vgg/software/via/via-1.0.6.html)을 활용해 Segmentation 영역 지정

1. Data Augmentation
    1. 좌우반전 (Flip)
    1. 180도 회전 (Rotation)
    1. 흑백처리 (Gray-Scale)

### 모델 선정 과정

1. Classification: Custom CNN, VGG, ResNet
    1. 단일 물체가 있는 정제된 데이터가 부족해 만족스러운 성능이 나오지 않았습니다. (65%)

1.  Object Detection: YOLO v3, Inception v3
    1. Pre-Trained: MS COCO
    1. 성능은 잘 나왔으나 물체가 겹쳐있을 경우 사용자가 Box만으로 물체를 구별하기 어려움

1. Segmentation: MaskRCNN
    1. Pre-Trained: MS COCO
    1. 물체에 직접 영역이 씌워져 대량의 물체가 겹쳐져있어도 구별하기 쉬움

### 웹

1. dash template을 flask에 적용하면서 요구사항에 맞추어 인터프리터 및 환경을 구축하며 눈물 한방울

1. 필요없는 부분을 지워야 하는데 연결되어 있는 함수 및 모듈이 복잡하여 지울 수 없었음에 눈물 한방울

1. 처음 보는 함수들과 많은 모듈이 거미줄처럼 엮여있어 흐름을 이해하는데 눈물 한방울(결국 이해불가)

1. dash와 flask를 동시에 활용함에 따른 app(server)의 결합에 눈물 한방울

1. 동적 처리를 위한 callback과 state에 대한 배경지식이 전무하여 눈물 한방울

## 결론

### 사용한 모델

1. MaskRCNN (Tensorflow, Pre-Trained: MS COCO)
1. Custom Data - 0000개
1. epoch
1. Loss

### 기대효과

1. 미흡한 분리배출로 발생하는 **경제적, 사회적 손실**을 줄이고자 함
    1. 재활용 쓰레기지만 일반쓰레기로 분류되어 발생하는 손실액이 연간 60억원입니다.
    1. 재활용 쓰레기를 확실히 분류하고, 정확한 분리배출 요령을 알려준다면 충분히 절약할 수 있습니다.
    1. 재활용될 수 있는 쓰레기를 매립, 소각함으로써 발생하는 환경문제도 줄일 수 있습니다.

### 활용방안

1. 개인
    1. 사용자 식별 기술과 하드웨어를 결합해 리워드를 제공하면 분리배출을 장려할 수 있다.
    1. 혼동되는 분리배출 요령을 실시간으로 쉽고 정확하게 알 수 있다.

1. 기관
    1. VR, AR을 결합해 선별작업을 수월하게 할 수 있다.

### 발전방향

1. 사용량이 많을수록 성능이 향상된다.
1. 데이터만 확보된다면 현재 3종류 이상의 쓰레기를 분류할 수 있다.

## 참조

- <https://tensorflow.blog/2017/06/05/from-r-cnn-to-mask-r-cnn/>
- <http://www.robots.ox.ac.uk/~vgg/software/via/via-1.0.6.html>
- <https://github.com/aleju/imgaug>
- <https://github.com/matterport/Mask_RCNN>
- <https://www.youtube.com/watch?v=uUYR6IEm5VM>
- <https://github.com/CrookedNoob/Mask_RCNN-Multi-Class-Detection>
- <https://github.com/priya-dwivedi/Deep-Learning/tree/master/mask_rcnn_damage_detection>
- <https://www.nocutnews.co.kr/news/5159798>
- <https://brunch.co.kr/@hangganread/121>
- <http://benefit.is/17832>
- <http://www.superbin.co.kr/new/contents/product.php>
- <https://youtu.be/0XQtHSY4cCE?t=213>
