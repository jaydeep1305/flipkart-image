import re
import os
import sys
import json
import time
from loguru import logger
import requests
import shutil
from bs4 import BeautifulSoup, Comment

file_name = open("urls.txt", "r")
for url in file_name:
    logger.info(url)
    response = requests.get(url)
    response = response.content.decode()
    soup = BeautifulSoup(response,"lxml")
    product_name = soup.select("h1")[0].text
    product_name = re.sub('[^A-Za-z0-9 ]+', '', product_name)
    try:
        os.mkdir("images/"+product_name)
        logger.debug(product_name)
    except Exception as ex:
        logger.error(ex)
    json_data = soup.select("script#is_script")[0].text
    json_data = json_data.replace("window.__INITIAL_STATE__ = ","")
    json_data = json_data.strip()
    json_data = json_data[:-1]
    json_data = re.search('"multimediaComponents":\[(.*?)\],', json_data)
    json_data = "["+json_data.group(1)+"]"
    json_data = json.loads(json_data)
    i = 0
    for data in json_data:
        try:
            url = data['value']['url']
            url = url.replace("/{@width}","")
            url = url.replace("/{@height}","")
            url = url.replace("?q={@quality}","")

            path = "images/"+product_name+"/"+str(i)+".jpeg"
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)  
            logger.debug(url)
            i+=1
        except Exception as ex:
            logger.error(ex)
