import os
import copy
import json
import time
import numpy as np
from PIL import Image
from imageio import imwrite


class ImgAugment:
    def __init__(self, path_imgs=None, **kwargs):
        self.path_imgs = os.path.abspath(
            './imgs') if path_imgs is None else path_imgs

        # 이미지(jpg, png, jpeg, gif)만 보기
        img_type = ['jpg', 'png', 'jpeg']
        files = os.listdir(self.path_imgs)
        self.img_files = [_ for _ in files if _.split(
            ".")[-1].lower() in img_type]
        self.content_name = [_ for _ in files if _.split('.')[-1] == 'json'][0]

    @staticmethod
    def progress_bar(value, endvalue, stamp, bar_length=50):
        import sys

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write('\rPercent: [{0}] {1}%  Time: {2}'.format(
            arrow + spaces, int(round(percent * 100)), time.strftime('%M:%S', time.gmtime(stamp))))
        sys.stdout.flush()

    def flip(self, path_result=None):
        from imgaug.augmenters import Fliplr
        from imgaug.augmentables.polys import Polygon, PolygonsOnImage

        tic = time.time()

        path_result = os.path.join(
            self.path_imgs, '../flip_images') if path_result is None else path_result
        if not os.path.isdir(path_result):
            os.makedirs(path_result)

        with open(os.path.join(self.path_imgs, self.content_name), "r", encoding='utf-8') as f:
            content = json.load(f)
            print(f'total: {len(self.img_files)}  content: {len(content)}\n')

        aug = Fliplr(1.0)  # 100% Flip시켜주는 인스턴스
        # Flip된 이미지의 json파일을 만들어주기 위해 기존 content를 복사합니다.
        raw_content = copy.deepcopy(content)

        # 이미지 개수만큼 반복
        for n, img_name in enumerate(self.img_files, 1):
            raw_img = Image.open(os.path.join(self.path_imgs, img_name))
            img = np.array(raw_img.convert('RGBA'))  # 이미지
            img_size = str(os.path.getsize(
                os.path.join(self.path_imgs, img_name)))  # 파일 용량
            img_name_flip = f"flip_{img_name.split('.')[0]}.png"

            # Annotation 개수
            annotation = len(content[img_name+img_size]['regions'])

            # Annotation 개수만큼 반복
            for i in range(annotation):
                # 기존 json파일에서 x, y좌표가 있는 경로
                location = content[img_name +
                                   img_size]['regions'][str(i)]['shape_attributes']
                x = location['all_points_x']  # x 좌표모음
                y = location['all_points_y']  # y 좌표모음
                point = [_ for _ in zip(x, y)]  # (x, y)좌표모음
                # (x, y)좌표를 Segmentation으로 만들기 위해 Polygon type으로 바꿔줍니다.
                point = Polygon(point)
                # 원본 이미지와 크기가 같은 빈 이미지에 point만 찍어놓습니다. => Segmentation만 형성됩니다.
                segmentation = PolygonsOnImage([point], shape=img.shape)
                # 원본 이미지+Segmentation을 Flip합니다. => Flip된 이미지, Flip된 point(좌표)가 나옵니다.
                image_flip, point_flip = aug(
                    image=img, polygons=segmentation)

                # Annotation 개수에 상관없이 1번만 실행되는 구문입니다.
                if i == 0:
                    imwrite(os.path.join(
                        path_result, img_name_flip), image_flip)

                    img_size_flip = os.path.getsize(os.path.join(
                        path_result, img_name_flip))  # Flip된 이미지 파일 용량

                self.progress_bar(n, len(self.img_files), time.time()-tic)
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
                content[img_name+img_size]['size'] = img_size_flip
                # filename을 바꿔줍니다.
                content[img_name+img_size]['filename'] = img_name_flip
                # key를 바꿔줍니다.
                content[img_name_flip+img_size_flip] = content.pop(
                    img_name+img_size)

        # 모든 이미지, Annotation이 Flip되어 저장되었고, Flip된 이미지를 반영하는 json파일(content_flip)이 완성되었습니다.
        else:
            print("\n\nHappy New Year!")  # 해피뉴이어!
            # 수정이 완료된 content_flip을 기존 content와 합쳐줍니다.
            raw_content.update(content)

            # 합본 json파일을 저장합니다.
            with open(os.path.join(path_result, self.content_name), 'w', encoding='utf-8') as f:
                json.dump(raw_content, f)
                print(
                    f"Flip된 이미지: {len(self.img_files)} 중 {len([_ for _ in os.listdir(path_result) if _.split('.')[-1] =='png'])} 개")

    def gray_scale(self, path_result=None):
        tic = time.time()

        path_result = os.path.join(
            self.path_imgs, '../gray_images') if path_result is None else path_result
        if not os.path.isdir(path_result):
            os.makedirs(path_result)

        with open(os.path.join(self.path_imgs, self.content_name), "r", encoding='utf-8') as f:
            content = json.load(f)
            print(f'total: {len(self.img_files)}  content: {len(content)}\n')

        # 이미지 개수만큼 반복
        for n, img_name in enumerate(self.img_files, 1):
            raw_img = Image.open(os.path.join(self.path_imgs, img_name))
            img = raw_img.convert('LA')
            img_size = str(os.path.getsize(
                os.path.join(self.path_imgs, img_name)))  # 파일 용량

            img_name_gray = f"gray_{img_name.split('.')[0]}.png"
            img.save(os.path.join(path_result, img_name_gray))
            img_size_gray = os.path.getsize(os.path.join(
                path_result, img_name_gray))

            self.progress_bar(n, len(self.img_files), time.time()-tic)
            ################# content_flip의 size, filename, key를 바꿔줍니다. #################
            content[img_name+img_size]['size'] = img_size_gray  # size를 바꿔줍니다.
            # filename을 바꿔줍니다.
            content[img_name +
                    img_size]['filename'] = img_name_gray
            # key를 바꿔줍니다.
            content[img_name_gray+img_size_gray] = content.pop(
                img_name+img_size)
        else:
            print("\n\nHappy New Year!")  # 해피뉴이어!

            with open(os.path.join(path_result, self.content_name), 'w', encoding='utf-8') as f:
                json.dump(content, f)
                print(
                    f"Grayscale된 이미지: {len(self.img_files)} 중 {len([_ for _ in os.listdir(path_result) if _.split('.')[-1] =='png'])} 개")
