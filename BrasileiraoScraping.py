#Web Scraping com Python da tabela do brasileirão usando selenium
#imports necessarios
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import itertools
#Web Scraping com Python da tabela do brasileirão usando selenium

# setando o caminho do chromedriver
s = Service("C:/Program Files (x86)/chromedriver.exe")
driver = webdriver.Chrome(service=s)
#maximiza a janela
driver.maximize_window()
#dicionario que vai armazenar os dados
dic = {'P':[],'Time':[],'PTS':[],'J':[],'V':[],'E':[],'D':[],'GP':[],'GC':[],'SG':[],'CA':[],'CV':[],'A%':[]}
#lista com as chaves do dicionario para os stats
lista_chaves = ['J','V','E','D','GP','GC','SG','CA','CV','A%']
#lista que vai armazenar os stats.text
lista_stats = []
#iterador circular para as chaves do dicionario
chaves_circulares = itertools.cycle(lista_chaves)
#adiciona o site que eu quero acessar
driver.get('https://www.cbf.com.br/futebol-brasileiro')
#espera ate que o botao de aceitar os cookies esteja disponivel
try:
    accept_cookie = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.ID,'cookie-banner-lgpd-action'))
    )
        #clica no botao de aceitar os cookies
    accept_cookie.click()
except Exception as e:
    print(e)

try:
    #espera o botao de menu estar disponivel para aparecer a tabela completa 
    section_button = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.CLASS_NAME,'section-expand'))
    )
    #clica no botao de menu
    section_button.click()
    time.sleep(3)
    #pega a tabela inteira
    tables_list = driver.find_elements(By.XPATH, '//tr')
    #pega as posicoes
    posicoes = driver.find_elements(By.XPATH, '//tr/td/b')
    #pega os times
    times = driver.find_elements(By.XPATH, '//span[@class="hidden-xs"]')
    #pega os stats
    stats = driver.find_elements(By.XPATH, '//tr/td[position() >= 2 and position() <= 11]')
    #pega os pontos
    pts = driver.find_elements(By.XPATH, '//tbody/tr/th')
    #adiciona as posicoes na lista de acordo com a chave
    for posicao in posicoes:
        dic['P'].append(posicao.text)
    #adiciona os times na lista de acordo com a chave
    for time in times:
        dic['Time'].append(time.text)
    #verifica se os stats nao estao vazios, se nao estiverem adiciona na lista de stats. obs: isso eh feito para evitar que o programa quebre caso os stats nao estejam disponiveis
    if stats:
        #itera sobre todos os textos de stats e adiciona na lista de stats
        for stat in stats:  
            lista_stats.append(stat.text)
        #esse looping serve para adicionar os stats na lista de acordo com a chave
        
        for i in range(0,len(lista_stats),10):
            #itera sobre as chaves do dicionario e adiciona os stats na lista de acordo com a chave
            for j in range(10):
                #adiciona os stats na lista de acordo com a chave
                dic[next(chaves_circulares)].append(lista_stats[i+j])
    #adiciona os pontos na lista de acordo com a chave
    for pt in pts:
        dic['PTS'].append(pt.text)
finally:
    driver.quit()

#aqui começa a brincadeira com pandas
df = pd.DataFrame(dic)

#separando a coluna time em estado e time
df["Estado"] = df["Time"].str.split("-",expand=True)[1].str.replace(" ","") 
df["Time"] = df["Time"].str.split("-",expand=True)[0]
df

#mudar a posicao da coluna estado
df = df[['P', 'Time', 'Estado', 'PTS', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', 'CA', 'CV', 'A%']]
df
#salvando o arquivo em csv
df.to_csv('tabela_brasileirao.csv',index=False)

