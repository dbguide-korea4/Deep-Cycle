class SearchImgSE:
    def __init__(self, keywords, path='C:/imgs/'):
        self.query = '+'.join(keywords.split(' '))
        self.path = path

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
        con_type = resp.headers['Content-Type'].split('/')[1]
        
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(os.path.join(f'{path}{filename}.{con_type}'), 'wb') as fp:
            fp.write(resp.content)
            
        print(f'success: {filename}.{con_type}')

    def naver_imgs_se(self, n_round=10):
        from datetime import datetime

        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'
        driver = self.sel_driver(url)

        n_except = 0
        for n in range(n_round):
            try:
                driver.find_elements_by_css_selector('div.photo_grid div.img_area')[n].click()
                img_src = driver.find_element_by_css_selector('div.viewer img').get_attribute('src').split('&type')[0]
                
                timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                img_name = f'img{timestamp}_{self.query}{n}'
                
                self.imgs_save(img_src, img_name, self.path)
            except:
                print(f'failed: img{n}')
                n_except += 1
                pass
        else:
            for i in driver.window_handles:
                driver.switch_to_window(i)
                driver.close()
            
            print(f'\ndownload: {n_round - n_except} files safely done')

    def daum_imgs_se(self, n_round=10):
        from datetime import datetime

        url = f'https://search.daum.net/search?w=img&enc=utf8&q={self.query}'
        driver = self.sel_driver(url)

        n_except = 0
        for n in range(n_round):
            try:
                driver.find_elements_by_css_selector('div.cont_img div.wrap_thumb')[n].click()
                img_src = driver.find_element_by_css_selector('div.cont_viewer img').get_attribute('src')

                timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                img_name = f'img{timestamp}_{self.query}{n}'
                
                self.imgs_save(img_src, img_name, self.path)
            except:
                print(f'failed: img{n}')
                n_except += 1
                pass
        else:
            for i in driver.window_handles:
                driver.switch_to_window(i)
                driver.close()

            print(f'\ndownload: {n_round - n_except} files safely done')
    
    def google_imgs_se(self, n_round=10):
        import requests
        import time
        import json, os
        import urllib.request
        from bs4 import BeautifulSoup
        from selenium import webdriver
        
        driver = webdriver.Chrome()
        url= f'https://www.google.com/search?q=={self.query}&tbm=isch'
        driver.get(url)
        time.sleep(1)
        driver.find_elements_by_css_selector("#res #rg_s .rg_el")[1].click()
        n_except = 0
        b = 0
        
        for n in range(n_round):
            try:
                time.sleep(1)
                dom = BeautifulSoup(driver.page_source, "lxml")
                image_url = [_["src"] for _ in dom.select("#irc_cc .irc_mimg a img") if _.has_attr("src")]
                
                
                for a in range(len(image_url)):
                    try:
                        url = image_url[a]
                        outfile = f"img{a+b+1}.jpg"
                        if not os.path.isdir(self.path):
                            os.makedirs(self.path)
                        urllib.request.urlretrieve(url, self.path+outfile)
                    except:
                        pass
                #time.sleep(1)
                b = b+a+1
                driver.find_elements_by_css_selector("#irc-cl #irc-rac")[0].click()
                time.sleep(1)
                driver.find_elements_by_css_selector("#irc-cl #irc-rac")[0].click()
                time.sleep(1)
                driver.find_elements_by_css_selector("#irc-cl #irc-rac")[0].click()
            except:
                print(f'{n}번째에서 failed')
                pass
            
        driver.close()
