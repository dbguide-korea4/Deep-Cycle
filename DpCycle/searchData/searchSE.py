class SearchImgSE:
    def __init__(self, keywords, path=None):
        self.query = '+'.join(keywords.split(' '))
        self.path = self.get_download_path() if path is None else path

    @staticmethod
    def progress_bar(value, endvalue, stamp, bar_length=50):
        import sys
        import time

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write('\rPercent: [{0}] {1}%  Time: {2}'.format(
            arrow + spaces, int(round(percent * 100)), time.strftime('%M:%S', time.gmtime(stamp))))
        sys.stdout.flush()

    @staticmethod
    def get_download_path():
        import os
        """Returns the default downloads path for linux or windows"""

        if os.name == 'nt':
            import winreg

            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]

            return os.path.join(location, 'imgs\\')
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads\\imgs\\')

    @staticmethod
    def sel_driver(url):
        from selenium import webdriver

        driver = webdriver.Chrome()
        driver.get(url)

        return driver

    @staticmethod
    def closed_sel_windows(driver):
        for window in driver.window_handles:
            driver.switch_to_window(window)
            driver.close()

    @staticmethod
    def imgs_save(url, filename, path):
        import requests
        import os

        resp = requests.get(url)
        con_type = resp.headers['Content-Type'].split('/')[1].split(';')[0]

        if not os.path.isdir(path):
            os.makedirs(path)

        with open(os.path.join(f'{path}{filename}.{con_type}'), 'wb') as fp:
            fp.write(resp.content)

        print(f'success: {filename}.{con_type}')

    @staticmethod
    def src_to_array(src):
        import requests
        from matplotlib.pylab import imread
        from io import BytesIO

        resp = requests.get(src)
        arr = imread(BytesIO(resp.content),
                     format=resp.headers['Content-Type'].split('/')[1])

        return arr

    def naver_imgs_se(self, n_round=10, down=True):
        import time
        from numpy import array
        from datetime import datetime
        from bs4 import BeautifulSoup
        from selenium.common.exceptions import NoSuchElementException

        tic = time.time()
        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'
        driver = self.sel_driver(url)
        driver.find_element_by_css_selector(
            'div.photo_grid div.img_area').click()

        print('Collecting images...')

        img_src = []
        imgs_arr = []
        n_except = 0
        for n in range(n_round):
            try:
                dom = BeautifulSoup(driver.page_source, 'lxml')
                img_src.extend([_['src'] for _ in dom.select(
                    'div.viewer img') if _.has_attr('src')])

                self.progress_bar(n+1, n_round, time.time()-tic)

                try:
                    driver.find_element_by_css_selector(
                        'div.viewer_content a.btn_next span').click()
                except NoSuchElementException:
                    driver.find_element_by_css_selector(
                        'a.btn_more').click()
                except:
                    pass
            except KeyboardInterrupt:
                print('\nStop collecting!')
                break

        img_src = set(img_src)
        self.closed_sel_windows(driver)
        print(f'\n\nDownloading {len(img_src)} images...')

        for i, src in enumerate(img_src):
            if down is True:
                try:
                    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                    img_name = f'img{timestamp}_{self.query}{i}'

                    self.imgs_save(src, img_name, self.path)
                except KeyboardInterrupt:
                    print('\nStop downloading!')
                    break
                except:
                    print(f'failed: img{i}')
                    n_except += 1
                    pass
            else:
                imgs_arr.append(self.src_to_array(src))

        total = len(img_src) - n_except
        print(f'\n{total if total>0 else 0} files safely done')

        if down is False:
            return array(imgs_arr)

    def daum_imgs_se(self, n_round=10, down=True):
        import time
        from numpy import array
        from datetime import datetime
        from bs4 import BeautifulSoup
        from selenium.common.exceptions import NoSuchElementException

        tic = time.time()
        url = f'https://search.daum.net/search?w=img&enc=utf8&q={self.query}'
        driver = self.sel_driver(url)
        driver.find_element_by_css_selector(
            'div.cont_img div.wrap_thumb').click()

        print('Collecting images...')

        img_src = []
        imgs_arr = []
        n_except = 0
        for n in range(n_round):
            try:
                dom = BeautifulSoup(driver.page_source, 'lxml')
                img_src.extend([_['src'] for _ in dom.select(
                    'div.cont_viewer div.inner_thumb img:last-child') if _.has_attr('src')])

                self.progress_bar(n+1, n_round, time.time()-tic)

                try:
                    driver.find_element_by_css_selector('a.btn_next').click()
                except NoSuchElementException as e:
                    driver.find_element_by_css_selector(
                        'a.expender.open').click()
                    driver.find_elements_by_css_selector(
                        'div.cont_img div.wrap_thumb')[n].click()
                except:
                    pass
            except KeyboardInterrupt:
                print('\nStop collecting!')
                break

        img_src = set(img_src)
        self.closed_sel_windows(driver)
        print(f'\n\nDownloading {len(img_src)} images...')

        for i, src in enumerate(img_src):
            if down is True:
                try:
                    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                    img_name = f'img{timestamp}_{self.query}{i}'

                    self.imgs_save(src, img_name, self.path)
                except KeyboardInterrupt:
                    print('\nStop downloading!')
                    break
                except:
                    print(f'failed: img{i}')
                    n_except += 1
                    pass
            else:
                imgs_arr.append(self.src_to_array(src))

        total = len(img_src) - n_except
        print(f'\n{total if total>0 else 0} files safely done')

        if down is False:
            return array(imgs_arr)

    def google_imgs_se(self, down=True):
        import time
        import json
        from numpy import array
        from datetime import datetime
        from bs4 import BeautifulSoup
        from selenium.common.exceptions import NoSuchElementException

        tic = time.time()
        url = f'https://www.google.com/search?q={self.query}&tbm=isch'
        driver = self.sel_driver(url)

        print('Collecting images...')

        imgs_arr = []
        n_except = 0
        stamp = 0

        last_height = driver.execute_script(
            'return document.body.scrollHeight')
        while True:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')

            time.sleep(0.5)

            new_height = driver.execute_script(
                'return document.body.scrollHeight')
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector('input#smb').click()
                except:
                    stamp = time.time() - tic
                    break
            last_height = new_height

        print('Time: ', time.strftime('%M:%S', time.gmtime(stamp)))

        dom = BeautifulSoup(driver.page_source, 'lxml')
        img_src = {json.loads(_.text)['ou'] for _ in dom.find_all(
            'div', {'class': 'rg_meta'})}

        self.closed_sel_windows(driver)
        print(f'Downloading {len(img_src)} images...')

        for i, src in enumerate(img_src):
            if down is True:
                try:
                    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                    img_name = f'img{timestamp}_{self.query}{i}'

                    self.imgs_save(src, img_name, self.path)
                except KeyboardInterrupt:
                    print('\nStop downloading!')
                    break
                except:
                    print(f'failed: img{i}')
                    n_except += 1
                    pass
            else:
                imgs_arr.append(self.src_to_array(src))

        total = len(img_src) - n_except
        print(f'\n{total if total>0 else 0} files safely done')

        if down is False:
            return array(imgs_arr)
