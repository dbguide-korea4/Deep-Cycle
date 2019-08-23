import os
import copy
import json
import time
import numpy as np
import imageio
import imgaug as ia
from imgaug.augmentables.polys import Polygon, PolygonsOnImage


class ImgAgmet:
    def __init__(self, **kwargs):
        self.path_dir = os.path.abspath("./")
        # 이미지(jpg, png, jpeg, gif)만 보기
        self.img_type = ['jpg', 'png', 'jpeg']

    @staticmethod
    def progress_bar(value, endvalue, stamp, bar_length=50):
        import sys

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write('\rPercent: [{0}] {1}%  Time: {2}'.format(
            arrow + spaces, int(round(percent * 100)), time.strftime('%M:%S', time.gmtime(stamp))))
        sys.stdout.flush()

    def flip(self):
        tic = time.time()
        path_images = os.path.join(self.path_dir, "images")
        path_flip_images = os.path.join(self.path_dir, "flip_images")
        files = os.listdir(path_images)

        with open(os.path.join(path_images, "via_region_data.json"), "r", encoding='utf-8') as f:
            content = json.load(f)

        imgFiles = [_ for _ in files if _.split(
            ".")[-1].lower() in self.img_type]
        print(f'total: {len(imgFiles)}/{len(files)}  content: {len(content)}\n')

        flipFunc = ia.augmenters.Fliplr(1.0)  # 100% Flip시켜주는 인스턴스
        # Flip된 이미지의 json파일을 만들어주기 위해 기존 content를 복사합니다.
        content_flip = copy.deepcopy(content)

        # 이미지 개수만큼 반복
        for n, imgName in enumerate(imgFiles, 1):
            image = imageio.imread(os.path.join(path_images, imgName))  # 이미지
            imgSize = str(os.path.getsize(
                os.path.join(path_images, imgName)))  # 파일 용량
            # Annotation 개수
            annotation = len(content_flip[imgName+imgSize]['regions'])

            # Annotation 개수만큼 반복
            for i in range(annotation):
                # 기존 json파일에서 x, y좌표가 있는 경로
                location = content_flip[imgName +
                                        imgSize]['regions'][str(i)]['shape_attributes']
                x = location['all_points_x']  # x 좌표모음
                y = location['all_points_y']  # y 좌표모음
                point = [_ for _ in zip(x, y)]  # (x, y)좌표모음
                # (x, y)좌표를 Segmentation으로 만들기 위해 Polygon type으로 바꿔줍니다.
                point = Polygon(point)
                # 원본 이미지와 크기가 같은 빈 이미지에 point만 찍어놓습니다. => Segmentation만 형성됩니다.
                segmentation = PolygonsOnImage([point], shape=image.shape)
                # 원본 이미지+Segmentation을 Flip합니다. => Flip된 이미지, Flip된 point(좌표)가 나옵니다.
                image_flip, point_flip = flipFunc(
                    image=image, polygons=segmentation)

                # Annotation 개수에 상관없이 1번만 실행되는 구문입니다.
                if i == 0:
                    while True:
                        try:
                            # Flip된 이미지를 다운받습니다.
                            imageio.imwrite(os.path.join(
                                path_flip_images, f'flip_{imgName}'), image_flip[:, :, :3])
                        except IndexError:
                            print('\n', 'reprocess:', imgName, image_flip.shape, '\n')
                            image_flip = image_flip.reshape(
                                image_flip.shape[0], -1, 1)
                            continue
                        break

                    imgSize_flip = os.path.getsize(os.path.join(
                        path_flip_images, f'flip_{imgName}'))  # Flip된 이미지 파일 용량

                self.progress_bar(n, len(imgFiles), time.time()-tic)
                ################# content_flip의 x, y좌표를 바꿔줍니다. #################
                # Flip된 point의 x좌표모음을 Polygon type에서 list type으로 바꿔줍니다.
                x_flip = point_flip.polygons[0].xx_int.tolist()
                # Flip된 point의 y좌표모음을 Polygon type에서 list type으로 바꿔줍니다.
                y_flip = point_flip.polygons[0].yy_int.tolist()
                location['all_points_x'] = x_flip  # Flip된 x좌표로 바꿔줍니다.
                location['all_points_y'] = y_flip  # Flip된 y좌표로 바꿔줍니다.

            # 모든 Annotation의 좌표를 잘 바꿔줬다면 실행되는 구문입니다.
            else:
                ################# content_flip의 size, filename, key를 바꿔줍니다. #################
                # size를 바꿔줍니다.
                content_flip[imgName+imgSize]['size'] = imgSize_flip
                # filename을 바꿔줍니다.
                content_flip[imgName+imgSize]['filename'] = f'flip_{imgName}'
                # key를 바꿔줍니다.
                content_flip[f'flip_{imgName}{imgSize_flip}'] = content_flip.pop(
                    imgName+imgSize)

        # 모든 이미지, Annotation이 Flip되어 저장되었고, Flip된 이미지를 반영하는 json파일(content_flip)이 완성되었습니다.
        else:
            print("\n\nHappy New Year!")  # 해피뉴이어!
            print('Flip된 이미지:', len(os.listdir(path_images))-1,
                  '중', len(os.listdir(path_flip_images))-1, '개')

        # 수정이 완료된 content_flip을 기존 content와 합쳐줍니다.
        content.update(content_flip)

        # 합본 json파일을 저장합니다.
        with open(os.path.join(path_flip_images, 'flip_via_region_data.json'), 'w', encoding='utf-8') as f:
            json.dump(content, f)
