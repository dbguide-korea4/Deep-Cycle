class SearchImgSE:
    def __init__(self, keywords):
        self.query = '+'.join(keywords.split(' '))

    def naver_imgs_se(self, n_round=10):
        import requests
        import os
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from datetime import datetime

        driver = webdriver.Chrome()

        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'
        driver.get(url)

        n_except = 0
        for n in range(n_round):
            try:
                driver.find_elements_by_css_selector('div.photo_grid div.img_area')[n].click()

                img_src = driver.find_element_by_css_selector('div.viewer img').get_attribute('src').split('&type')[0]
                resp = requests.get(img_src)
                con_type = resp.headers['Content-Type'].split('/')[1]
                timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

                filename = f'img{timestamp}_{self.query}{n}.{con_type}'
                path = './imgs/'
                
                if not os.path.isdir(path):
                    os.makedirs(path)

                with open(os.path.join(f'{path}{filename}'), 'wb') as fp:
                    fp.write(resp.content)
                    print(f'success: {filename}')
            except:
                print(f'failed: img{n}')
                n_except += 1
                pass
        else:
            print(f'\ndownload: {n_round - n_except} files safely done')

        driver.close()

    def daum_imgs_se(self, n_round=10):
        import requests
        import os
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from datetime import datetime

        driver = webdriver.Chrome()

        url = f'https://search.daum.net/search?w=img&enc=utf8&q={self.query}'
        driver.get(url)

        n_except = 0
        for n in range(n_round):
            try:
                driver.find_elements_by_css_selector('div.cont_img div.wrap_thumb')[n].click()

                img_src = driver.find_element_by_css_selector('div.cont_viewer img').get_attribute('src')
                resp = requests.get(img_src)
                con_type = resp.headers['Content-Type'].split('/')[1]
                timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

                filename = f'img{timestamp}_{self.query}{n}.{con_type}'
                path = './imgs/'
                
                if not os.path.isdir(path):
                    os.makedirs(path)

                with open(os.path.join(f'{path}{filename}'), 'wb') as fp:
                    fp.write(resp.content)
                    print(f'success: {filename}')
            except:
                print(f'failed: img{n}')
                n_except += 1
                pass
        else:
            print(f'\ndownload: {n_round - n_except} files safely done')

        driver.close()

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
                        outpath = "D:/google_crawling/"
                        outfile = f"img{a+b+1}.jpg"
                        if not os.path.isdir(outpath):
                            os.makedirs(outpath)
                        urllib.request.urlretrieve(url, outpath+outfile)
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