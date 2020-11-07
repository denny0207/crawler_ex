import os
import requests
# requests V2.21.0
from bs4 import BeautifulSoup as bs
# beautifulsoup4 V4.8.0
import logging
logging.basicConfig(filename='sign_in.log', level=logging.DEBUG, 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

ppath = os.path.dirname(os.path.realpath('__file__'))
os.chdir(ppath)

# 保存 cookie
session = requests.Session()


# 登录
def login_hacpai():
    login_url = 'https://ld246.com/login'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 
               'Referer':'https://ld246.com/login'}

    raw_data = {"captcha":""}

    with open('pwd') as f:
        # for line in f.readlines():
        #     data_ls = []
        #     datas = line.replace('\n', '')
        #     data_ls = datas.split(',')
        #     raw_data[data_ls[0]] = data_ls[1]
        
        line_ls = f.readlines()
        data_ls = list(map(lambda x: x.replace('\n', ''), line_ls))
        raw_data = {i.split(',')[0]:i.split(',')[1]  for i in data_ls}

    try:
        request = session.post(login_url, headers=headers, json=raw_data)
        request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.debug(err)
        print('登录失败!','HTTPError: {}'.format(err))
    except Exception as err:
        logger.debug(err)
        print('登录失败!', 'error: {}'.format(err))
    else:
        # result = request.text.replace("{","").split(',')
        result = request.text.split(',')
        respons_ls = result[:2]
        result_ls = [ i.split(':')[1] for i in respons_ls]
        return result_ls


# 获取签到链接
def get_url():
    url = 'https://ld246.com/activity/daily-checkin'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Referer':'https://ld246.com/'}
    try:
        request = session.get(url, headers=headers)
        respons = request.text
        class_= "module__body ft__center vditor-reset"
        soup = bs(respons, 'lxml').find('div', class_=class_)
        # sign_url_soup = soup.find_all('a', class_="btn green")
        for i in soup('a'):
            link = i.get('href')
        return link
    except (SyntaxError, ImportError,
            UnicodeEncodeError, AttributeError) as err:
        logger.debug(err)    
        print('error: {}'.format(err))
    except Exception as err:
        logger.debug(err)
        print('请求失败!', 'error: {}'.format(err))


# 签到
def sign(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Referer':'https://ld246.com/activity/checkin'}
   
    try:
        request = session.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.debug(err)
        print('请求失败!','HTTPerror: {}'.format(err))
    except Exception as err:
        logger.debug(err)
        print('请求失败!', 'error: {}'.format(err))
    else:
        respons = request.text
        soup = bs(respons, 'lxml').find('div', class_="vditor-reset")
        for s in soup.div.strings:
            s = s.replace(' ', '')
            print(s,end=' ')
    

def main():
    sign_in_url = 'https://ld246.com/activity/checkin'
    result_ls = login_hacpai()
    if result_ls[0] == 'false':
        print('登录失败!', result_ls[1], sep='\n')

    else:
        print('登录成功!')
        url = get_url()
        if url == None:
            print('未找到签到链接。')
        elif 'points' in url:
            print('今日你已经签过到了。')
            print('可以点击或复制链接：{} 查看'.format(sign_in_url))
        else:
            sign(url)


if __name__ == "__main__":
    logger.info('Started..')
    #main()
    logger.info("Finished!\n")
    

    


