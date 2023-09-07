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

# colecao ="https://www.thingiverse.com/chriscoliveira/collections"
# colecao1="https://www.thingiverse.com/chriscoliveira/collections/39300680/things" #magic
# colecao2="https://www.thingiverse.com/chriscoliveira/collections/39270603/things" #legais
# colecao3="https://www.thingiverse.com/chriscoliveira/collections/39258142/things" #nerd
# colecao4="https://www.thingiverse.com/chriscoliveira/collections/39306277/things" #ender
# abre as configs do chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    "excludeSwitches", ['enable-logging'])

current_dateTime = datetime.now()


def pegaLinksThingiverse(url, pasta):
    pasta = pasta.upper()
    print(f'Procurando na coleção {pasta}')
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
        navegador.find_element(
            'xpath', '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
    except:
        pass

    # navega ate p fim da pagina
    t = navegador.find_element(by=By.TAG_NAME, value='body')
    for i in range(30):
        t.send_keys(Keys.END)
        sleep(2)

    # captura os itens da pagina
    sleep(5)
    resultado = navegador.find_element(
        'xpath', '/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]')
    resultado = resultado.get_attribute('innerHTML')
    navegador.close()

    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'CardGrid__cardGridItem--JlDk9'})

    with open('titulos.txt', 'a+') as gravaarquivo:

        with open('titulos.txt', 'r') as lerarquivo:
            lerarquivo = lerarquivo.readlines()

            for i in itens:
                links = i.find_all(
                    'a', {'class': 'ThingCardBody__cardBodyWrapper--BLLzJ'})
                for link in links:

                    # baixa a imagem do arquivo
                    titulo = i.find(
                        'span', {'class': 'ThingCardHeader__cardNameWrapper--VgmUP'})['title']
                    foto = i.find('img', {'alt': 'Make Card'})
                    titulo = titulo.replace('\(', '').replace('\)', '').replace(
                        '/', '').replace(':', '').replace('|', '')
                    endereco = link['href']

                    # SE O ITEM FOR NOVO
                    if not f"{endereco}\n" in lerarquivo:
                        # CRIA O TXT COM O COMENTARIO DO AUTOR
                        navegador1 = webdriver.Chrome(options=chrome_options)
                        navegador1.set_window_size(1920, 1080)
                        navegador1.get(str(endereco))
                        sleep(3)
                        
                        resultado_link = navegador1.find_element(
                            'xpath', '/html/body/div[2]/div/div/div[3]/div/div[3]/div[2]/div[1]/div[2]')
                        resultado_link = resultado_link.get_attribute(
                            'innerText')
                        with open(f'{pasta}/{titulo}.txt', 'w') as f:
                            f.write(resultado_link)
                        navegador1.close()

                        # ADICIONA O NOME DO MODELO
                        with open('modelos.txt', 'a+') as model:
                            model.write(f"{pasta} >> {titulo} -> {endereco}\n")

                        gravaarquivo.write(f"{endereco}\n")
                        x = endereco.split(':')[2]
                        print(f'Novo item: {pasta}>{titulo}:{endereco}')

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

                        r = requests.get(file_url, stream=True)
                        with open(f"{pasta}/{titulo}.zip", "wb") as stl:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    stl.write(chunk)
                    else:
                        ...


def pegaColecao(usuario):
    url = f"https://www.thingiverse.com/{usuario}/collections"
    print(f'Captura modelos no site Thingiverse\n\nColeção: {url}\n\n')
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.set_window_size(1920, 1080)
    navegador.get(url)
    sleep(3)
    resultado = navegador.find_element(
        'xpath', '//*[@id="react-app"]/div/div/div[3]/div/div/div[2]/div[2]')

    resultado = resultado.get_attribute('innerHTML')
    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'CardGrid__cardGridItem--JlDk9'})
    lista = []
    for i in itens:

        link = i.find(
            'a', {'class': 'CollectionCardBody__cardBodyWrapper--quaCB'})['href']
        span = i.find(
            'span', {'class': 'CollectionCardHeader__cardNameWrapper--CSZ25'}).text
        print(f'Coleção encontrada: {span}\n')
        lista.append([link, str(span).upper()])

    for i in lista:
        pegaLinksThingiverse(i[0], i[1])


def pegaLinksPrintable(url, pasta):
    pasta = pasta.upper()
    print(f'Procurando na coleção {pasta}')
    try:
        os.mkdir(pasta)
    except:
        pass

    navegador = webdriver.Chrome(options=chrome_options)
    navegador.set_window_size(1920, 1080)
    navegador.get(url)
    sleep(3)

    # navega ate p fim da pagina
    t = navegador.find_element(by=By.TAG_NAME, value='body')
    for i in range(30):
        t.send_keys(Keys.END)
        sleep(2)

    # captura os itens da pagina
    sleep(5)
    resultado = navegador.find_element(
        'xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-sticky-sidebar/main/div/div/div[2]/collection-detail/app-load-more-infinity-with-placeholder/div/div[1]/div')
    resultado = resultado.get_attribute('innerHTML')
    navegador.close()

    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'print-list-item'})

    with open('titulos.txt', 'a+') as gravaarquivo:

        with open('titulos.txt', 'r') as lerarquivo:
            lerarquivo = lerarquivo.readlines()

            for i in itens:
                links = i.find_all('a', {'class': 'link clamp-two-lines'})
                for link in links:

                    # baixa a imagem do arquivo
                    titulo = i.find('h3', {'class': 'name no-category'}).text
                    try:
                        foto = i.find_all('img')[1]
                    except:
                        pass
                    titulo = titulo.replace('\(', '').replace('\)', '').replace(
                        '/', '').replace(':', '').replace('|', '')
                    endereco = 'https://www.printables.com'+link['href']

                    # print(titulo,foto,endereco)

                    # SE O ITEM FOR NOVO
                    if not f"{endereco}\n" in lerarquivo:
                        # CRIA O TXT COM O COMENTARIO DO AUTOR
                        navegador1 = webdriver.Chrome(options=chrome_options)
                        navegador1.set_window_size(1920, 1080)
                        navegador1.get(str(endereco))

                        sleep(5)
                        navegador1.find_element(
                            'xpath', '/html/body/div[1]/div[2]/div/div/div[2]/div/div/button').click()
                        sleep(1)
                        resultado_link = navegador1.find_element(
                            'xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/main/market-summary/div')
                        resultado_link = resultado_link.get_attribute(
                            'innerText')
                        with open(f'{pasta}/{titulo}.txt', 'w') as f:
                            f.write(resultado_link)

                        navegador1.find_element(
                            'xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/div[1]/div/div[2]/a').click()
                        sleep(3)

                        ll = navegador1.find_element(
                            'xpath', '/html/body/app-root/app-baselayout/div/ng-component/app-market-detail/main/app-market-files/div/app-market-downloads/div[1]')
                        ll = ll.get_attribute('innerHTML')

                        soup = BeautifulSoup(ll, 'html.parser')
                        down = soup.find('a', {'class': 'btn btn-outline'})

                        # ADICIONA O NOME DO MODELO
                        with open('modelos.txt', 'a+') as model:
                            model.write(f"{pasta} >> {titulo} -> {endereco}\n")

                        gravaarquivo.write(f"{endereco}\n")
                        # x= endereco.split(':')[2]
                        print(f'Novo item: {pasta}>{titulo}:{endereco}')

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
                        try:
                            r = requests.get(down['href'], stream=True, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
                            with open(f"{pasta}/{titulo}.zip", "wb") as stl:
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:
                                        stl.write(chunk)
                        except:
                            pass
                    else:
                        ...


# pegaLinksPrintable(
#     'https://www.printables.com/@ChristiandeC_1202133/collections/827366', 'printables')
pegaColecao('chriscoliveira')
# pegaLinks("https://www.thingiverse.com/chriscoliveira/collections/39300680/things","a")
