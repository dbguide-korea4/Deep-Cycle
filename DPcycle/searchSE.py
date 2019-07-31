class Search:
    def __init__(self, keywords):
        self.query = '+'.join(keywords.split(' '))
    
    def naver_imgs_se(self, n_round=10):
        import requests, os
        from bs4 import BeautifulSoup
        from selenium import webdriver
        
        driver = webdriver.Chrome()
        
        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'
        driver.get(url)
        
        n_except = 0
        for n in range(n_round):
            try:
                driver.find_elements_by_css_selector("div.photo_grid div.img_area")[n].click()

                img_src = driver.find_element_by_css_selector("div.viewer img").get_attribute('src').split('&type')[0]
                resp = requests.get(img_src)
                con_type = resp.headers['Content-Type'].split('/')[1]

                with open(os.path.join(f'./imgs/img{n}.{con_type}'), 'wb') as fp:
                    fp.write(resp.content)
                    print(f'success: img{n}.{con_type}')
            except:
                print(f'failed: img{n}')
                n_except += 1
                pass
        else:
            return f'download: {n_round - n_except} files safely done'
            
        driver.close()