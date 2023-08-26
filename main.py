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

colecao1="https://www.thingiverse.com/chriscoliveira/collections/39300680/things" #magic
colecao2="https://www.thingiverse.com/chriscoliveira/collections/39270603/things" #legais
colecao3="https://www.thingiverse.com/chriscoliveira/collections/39258142/things" #nerd
colecao4="https://www.thingiverse.com/chriscoliveira/collections/39306277/things" #ender
# abre as configs do chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
                "excludeSwitches", ['enable-logging'])

def pegaLinks(url,pasta):
    pasta=pasta.upper()
    print(pasta)
    try:
        os.mkdir(pasta)
    except:
        pass

    navegador = webdriver.Chrome(options=chrome_options)
    navegador.set_window_size(1920, 1080)
    navegador.get(url)
    sleep(3)

    # clica em permitir cookies
    try:
        navegador.find_element('xpath', '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
    except:
        pass
    
    #navega ate p fim da pagina
    t = navegador.find_element(by=By.TAG_NAME,value='body')
    for i in range(30):
        t.send_keys(Keys.END)
        sleep(2)

    #captura os itens da pagina
    sleep(5)
    resultado = navegador.find_element('xpath', '/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]')
    
    resultado = resultado.get_attribute('innerHTML')
    
    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'CardGrid__cardGridItem--JlDk9'})

    
    with open('titulos.txt', 'a+') as gravaarquivo:

        with open('titulos.txt', 'r') as lerarquivo:
            lerarquivo = lerarquivo.readlines()
            
            for i in itens:
                links = i.find_all('a',{'class':'ThingCardBody__cardBodyWrapper--BLLzJ'})
                for link in links:
                    # baixa a imagem do arquivo
                    titulo = i.find('span', {'class':'ThingCardHeader__cardNameWrapper--VgmUP'})['title']
                    foto = i.find('img', {'alt':'Make Card'})
                    titulo = titulo.replace('\(','').replace('\)','').replace('/','')
                    
                    endereco = link['href']
                    
                    
                    # SE O ITEM FOR NOVO
                    if not f"{endereco}\n" in lerarquivo:
                        gravaarquivo.write(f"{endereco}\n")
                        x= endereco.split(':')[2]
                        print(pasta,titulo,endereco)
                        # baixa a imagem do arquivo
                        with open(f'{pasta}/{titulo}.jpg', 'wb') as handle:
                            response = requests.get(foto['src'], stream=True, headers={
                                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
                            if not response.ok:
                                response
                            for block in response.iter_content(1024):
                                if not block:
                                    break
                                handle.write(block)
                        
                        # baixa o arquivo
                        file_url = f'https://tv-zip.thingiverse.com/zip/{x}'
                        
                        r = requests.get(file_url,stream=True)
                        with open(f"{pasta}/{titulo}.zip","wb") as stl: 
                            for chunk in r.iter_content(chunk_size=1024): 
                                if chunk: 
                                    stl.write(chunk) 
                    else:
                        ...

                    

                    ## permite os cookies e baixa o anexo na pasta download do navegador
                    # navegador.get(link['href'])
                    # sleep(5)
                    # try:
                    #     navegador.find_element('xpath', '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
                    # except:
                    #     pass
                    # navegador.find_element(By.XPATH, '//button[text()="Download All Files"]').click()
                    
                    # sleep(35)

pegaLinks(colecao1,'MAGIC')
pegaLinks(colecao2,'LEGAIS')
pegaLinks(colecao3,'NERD')
pegaLinks(colecao4,'ENDER')

