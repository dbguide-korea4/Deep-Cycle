class SearchImgSE:
    def __init__(self, keywords, path=None):
        self.query = '+'.join(keywords.split(' '))
        self.path = self.get_download_path() if path is None else path

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
    def src_to_array(scr):
        import requests
        from matplotlib.pylab import imread
        from io import BytesIO

        resp = requests.get(url)
        arr = imread(BytesIO(resp.content),
                    format=resp.headers['Content-Type'].split('/')[1])

        return arr

    def naver_imgs_se(self, n_round=10, down=True):
        from numpy import array
        from datetime import datetime

        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'
        driver = self.sel_driver(url)

        img_src = []
        imgs_arr = []
        n_except = 0
        for n in range(n_round):
            driver.find_elements_by_css_selector(
                'div.photo_grid div.img_area')[n].click()
            img_src.append(driver.find_element_by_css_selector(
                'div.viewer img').get_attribute('src').split('&type')[0])
        else:
            for i, src in enumerate(set(img_src)):
                if down is True:
                    try:
                        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                        img_name = f'img{timestamp}_{self.query}{i}'

                        self.imgs_save(src, img_name, self.path)
                    except:
                        print(f'failed: img{i}')
                        n_except += 1
                        pass
                else:
                    imgs_arr.append(self.src_to_array(src))

        for window in driver.window_handles:
                driver.switch_to_window(window)
                driver.close()

        if down is False:
            return array(imgs_arr)
        
        print(f'\n{n_round - n_except} files safely done')

    def daum_imgs_se(self, n_round=10, down=True):
        from numpy import array
        from datetime import datetime

        url = f'https://search.daum.net/search?w=img&enc=utf8&q={self.query}'
        driver = self.sel_driver(url)

        img_src = []
        imgs_arr = []
        n_except = 0
        for n in range(n_round):
            driver.find_elements_by_css_selector(
                'div.cont_img div.wrap_thumb')[n].click()
            img_src.append(driver.find_element_by_css_selector(
                'div.cont_viewer img').get_attribute('src'))
        else:
            for i, src in enumerate(set(img_src)):
                if down is True:
                    try:
                        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                        img_name = f'img{timestamp}_{self.query}{i}'

                        self.imgs_save(src, img_name, self.path)
                    except:
                        print(f'failed: img{i}')
                        n_except += 1
                        pass
                else:
                    imgs_arr.append(self.src_to_array(src))


        for window in driver.window_handles:
            driver.switch_to_window(window)
            driver.close()

        if down is False:
            return array(imgs_arr)

        print(f'\n{n_round - n_except} files safely done')

    def google_imgs_se(self, n_round=10, down=True):
        from bs4 import BeautifulSoup
        from numpy import array
        from datetime import datetime

        url = f'https://www.google.com/search?q={self.query}&tbm=isch'
        driver = self.sel_driver(url)
        driver.find_element_by_css_selector('div#rg_s div.rg_el').click()

        img_src = []
        imgs_arr = []
        n_except = 0
        for n in range(n_round):
            dom = BeautifulSoup(driver.page_source, "lxml")
            img_src.extend([_['src'] for _ in dom.select(
                'div#irc_cc div.irc_mimg img') if _.has_attr('src')])

            driver.find_element_by_css_selector('#irc-cl #irc-rac').click()
        else:
            for i, src in enumerate(set(img_src)):
                if down is True:
                    try:
                        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                        img_name = f'img{timestamp}_{self.query}{i}'

                        self.imgs_save(src, img_name, self.path)
                    except:
                        print(f'failed: img{i}')
                        n_except += 1
                        pass
                else:
                    imgs_arr.append(self.src_to_array(src))

        for window in driver.window_handles:
                driver.switch_to_window(window)
                driver.close()
        
        if down is False:
            return array(imgs_arr)

        print(f'\n{n_round - n_except} files safely done')
