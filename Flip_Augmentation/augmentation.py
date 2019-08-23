import os
import copy
import json
import time
import numpy as np
from PIL import Image
from imageio import imwrite


class ImgAgmet:
    def __init__(self, path=None, **kwargs):
        self.path_dir = os.path.abspath("./") if path is None else path
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

    def flip(self, path='flip_images'):
        from imgaug.augmenters import Fliplr
        from imgaug.augmentables.polys import Polygon, PolygonsOnImage

        tic = time.time()

        path_images = os.path.join(self.path_dir, "images")
        path_result = os.path.join(self.path_dir, path)

        if not os.path.isdir(path_result):
            os.makedirs(path_result)

        files = os.listdir(path_images)
        img_files = [_ for _ in files if _.split(
            ".")[-1].lower() in self.img_type]
        with open(os.path.join(path_images, "via_region_data.json"), "r", encoding='utf-8') as f:
            content = json.load(f)

        print(
            f'total: {len(img_files)}  content: {len(content)}\n')

        aug = Fliplr(1.0)  # 100% Flip시켜주는 인스턴스
        # Flip된 이미지의 json파일을 만들어주기 위해 기존 content를 복사합니다.
        raw_content = copy.deepcopy(content)

        # 이미지 개수만큼 반복
        for n, img_name in enumerate(img_files, 1):
            raw_img = Image.open(os.path.join(path_images, img_name))
            img = np.array(raw_img.convert('RGB'))  # 이미지
            img_size = str(os.path.getsize(
                os.path.join(path_images, img_name)))  # 파일 용량
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
                        path_result, f'flip_{img_name}'), image_flip[:, :, :3])

                    img_size_flip = os.path.getsize(os.path.join(
                        path_result, f'flip_{img_name}'))  # Flip된 이미지 파일 용량

                self.progress_bar(n, len(img_files), time.time()-tic)
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
                content[img_name+img_size]['filename'] = f'flip_{img_name}'
                # key를 바꿔줍니다.
                content[f'flip_{img_name}{img_size_flip}'] = content.pop(
                    img_name+img_size)

        # 모든 이미지, Annotation이 Flip되어 저장되었고, Flip된 이미지를 반영하는 json파일(content_flip)이 완성되었습니다.
        else:
            print("\n\nHappy New Year!")  # 해피뉴이어!
            # 수정이 완료된 content_flip을 기존 content와 합쳐줍니다.
            raw_content.update(content)

            # 합본 json파일을 저장합니다.
            with open(os.path.join(path_result, 'flip_via_region_data.json'), 'w', encoding='utf-8') as f:
                json.dump(raw_content, f)

        print('Flip된 이미지:', len(img_files),
              '중', len(os.listdir(path_result))-1, '개')

    def gray_scale(self, path='gray_images'):
        from imgaug.augmenters import Grayscale
        tic = time.time()

        path_images = os.path.join(self.path_dir, "images")
        path_result = os.path.join(self.path_dir, path)

        if not os.path.isdir(path_result):
            os.makedirs(path_result)

        files = os.listdir(path_images)
        img_files = [_ for _ in files if _.split(
            ".")[-1].lower() in self.img_type]
        with open(os.path.join(path_images, "via_region_data.json"), "r", encoding='utf-8') as f:
            content = json.load(f)

        print(
            f'total: {len(img_files)}  content: {len(content)}\n')

        aug = Grayscale(alpha=1)  # 그레이스케일
        # 그레이스케일된 이미지의 json파일을 만들어주기 위해 기존 content를 복사합니다.
        raw_content = copy.deepcopy(content)

        # 이미지 개수만큼 반복
        for n, img_name in enumerate(img_files, 1):
            raw_img = Image.open(os.path.join(path_images, img_name))
            img = np.array(raw_img.convert('RGB'))
            img_size = str(os.path.getsize(
                os.path.join(path_images, img_name)))  # 파일 용량

            img_aug = aug(image=img)

            imwrite(os.path.join(path_result,
                                 f'gray_{img_name}'), img_aug[:, :, :3])
            img_size_gray = os.path.getsize(os.path.join(
                path_result, f'gray_{img_name}'))  # Flip된 이미지 파일 용량

            self.progress_bar(n, len(img_files), time.time()-tic)
            ################# content_flip의 size, filename, key를 바꿔줍니다. #################
            content[img_name+img_size]['size'] = img_size_gray  # size를 바꿔줍니다.
            # filename을 바꿔줍니다.
            content[img_name+img_size]['filename'] = f'gray_{img_name}'
            # key를 바꿔줍니다.
            content[f'gray_{img_name}{img_size_gray}'] = content.pop(
                img_name+img_size)
        else:
            print("\n\nHappy New Year!")  # 해피뉴이어!
            raw_content.update(content)

            with open(os.path.join(path_result, 'gray_via_region_data.json'), 'w', encoding='utf-8') as f:
                json.dump(raw_content, f)

        print('Grayscale된 이미지:', len(img_files),
              '중', len(os.listdir(path_result))-1, '개')