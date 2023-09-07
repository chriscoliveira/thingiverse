# lista = ['https://www.thingiverse.com/thing:6154327\n', 'https://www.thingiverse.com/thing:213990\n', 'https://www.thingiverse.com/thing:2975065\n', 'https://www.thingiverse.com/thing:3928643\n', 'https://www.thingiverse.com/thing:2271264\n', 'https://www.thingiverse.com/thing:955433\n', 'https://www.thingiverse.com/thing:909499\n', 'https://www.thingiverse.com/thing:324433\n', 'https://www.thingiverse.com/thing:3940310\n', 'https://www.thingiverse.com/thing:2936081\n', 'https://www.thingiverse.com/thing:3680311\n', 'https://www.thingiverse.com/thing:23464\n', 'https://www.thingiverse.com/thing:1092181\n', 'https://www.thingiverse.com/thing:1376811\n', 'https://www.thingiverse.com/thing:10483\n', 'https://www.thingiverse.com/thing:1790624\n', 'https://www.thingiverse.com/thing:2369887\n', 'https://www.thingiverse.com/thing:919475\n', 'https://www.thingiverse.com/thing:2014307\n', 'https://www.thingiverse.com/thing:5254334\n', 'https://www.thingiverse.com/thing:5428627\n', 'https://www.thingiverse.com/thing:3587429\n', 'https://www.thingiverse.com/thing:3296608\n', 'https://www.thingiverse.com/thing:1563645\n', 'https://www.thingiverse.com/thing:3054701\n', 'https://www.thingiverse.com/thing:1499047\n', 'https://www.thingiverse.com/thing:2815721\n', 'https://www.thingiverse.com/thing:5341335\n', 'https://www.thingiverse.com/thing:5548089\n', 'https://www.thingiverse.com/thing:3604104\n', 'https://www.thingiverse.com/thing:1028742\n', 'https://www.thingiverse.com/thing:6158720\n', 'https://www.thingiverse.com/thing:6140273\n', 'https://www.thingiverse.com/thing:6133245\n', 'https://www.thingiverse.com/thing:6122447\n', 'https://www.thingiverse.com/thing:6130586\n', 'https://www.thingiverse.com/thing:6145669\n', 'https://www.thingiverse.com/thing:6155544\n', 'https://www.thingiverse.com/thing:6138559\n', 'https://www.thingiverse.com/thing:6160974\n', 'https://www.thingiverse.com/thing:6140285\n', 'https://www.thingiverse.com/thing:6135023\n', 'https://www.thingiverse.com/thing:6130163\n', 'https://www.thingiverse.com/thing:6147150\n', 'https://www.thingiverse.com/thing:6124479\n', 'https://www.thingiverse.com/thing:6152817\n', 'https://www.thingiverse.com/thing:6139922\n', 'https://www.thingiverse.com/thing:6125305\n', 'https://www.thingiverse.com/thing:6127792\n', 'https://www.thingiverse.com/thing:6140618\n', 'https://www.thingiverse.com/thing:6120691\n', 'https://www.thingiverse.com/thing:6155089\n', 'https://www.thingiverse.com/thing:6138737\n', 'https://www.thingiverse.com/thing:6134800\n', 'https://www.thingiverse.com/thing:6137324\n', 'https://www.thingiverse.com/thing:6133782\n', 'https://www.thingiverse.com/thing:6142670\n', 'https://www.thingiverse.com/thing:6129076\n', 'https://www.thingiverse.com/thing:6139025\n', 'https://www.thingiverse.com/thing:6145908\n', 'https://www.thingiverse.com/thing:6121689\n', 'https://www.thingiverse.com/thing:6121644\n']

# for i in lista:
#     if 'https://www.thingiverse.com/thing:61543271' in i:
#         print('igual')
    

# import requests
# file_url = 'https://tv-zip.thingiverse.com/zip/5804636'

# r = requests.get(file_url,stream=True)
# with open("python.zip","wb") as stl: 
#     for chunk in r.iter_content(chunk_size=1024): 
#         if chunk: 
#             stl.write(chunk) 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from time import sleep
from natsort import natsorted
import zipfile
import zipfile as zipf
import os
import colorama
import glob
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
                "excludeSwitches", ['enable-logging'])

current_dateTime = datetime.now()
pasta='PRINTABLES'
titulo='teste'
endereco='https://www.printables.com/model/274935-baby-groot'
navegador1 = webdriver.Chrome(options=chrome_options)
navegador1.set_window_size(1920, 1080)
navegador1.get(str(endereco))

sleep(2)
navegador1.find_element('xpath','/html/body/div[1]/div[2]/div/div/div[2]/div/div/button').click()
sleep(1)
resultado_link = navegador1.find_element('xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/main/market-summary/div')
resultado_link = resultado_link.get_attribute('innerText')  
with open(f'{pasta}/{titulo}.txt','w') as f:
    f.write(resultado_link)

navegador1.find_element('xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/div[1]/div/div[2]/a').click()
sleep(3)

ll = navegador1.find_element('xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/main/app-market-files/div/app-market-downloads/div[1]')
ll = ll.get_attribute('innerHTML')  

soup = BeautifulSoup(ll, 'html.parser')
itens = soup.find_all('a',{'class':'btn btn-outline'})
for i in itens:
    r = requests.get(i['href'],stream=True)
    with open(f"{pasta}/{titulo}.zip","wb") as stl: 
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                stl.write(chunk) 

sleep(5)