import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
os.system('cls')

def busca_salarios_glassdoor(url):
    # Definindo um Browser como agente de busca 
    hearders = {'user-agent' : 'Chrome'}

    # Fazendo a requisição do conteudo da url utilizando o chrome como user agent
    resposta = requests.get(url,
                            headers=hearders)
    print(resposta) # Para verificar o codigo de retorno da requisição
    
    # Estrutura do site
    web_scrapy = resposta.text

    # Criando a estrutura hierarquica da pagina html
    beaut_web_scrapy = BeautifulSoup(web_scrapy, 'html.parser')

    # Procurando todas estruturas que possuem o data-test especifico do nome das empresas e dos salarios
    lista_empresas = beaut_web_scrapy.find_all('h3', {'data-test':re.compile('salaries-list-item-.*-employer-name')})
    lista_salarios = beaut_web_scrapy.find_all('div', {'data-test':re.compile('salaries-list-item-.*-salary-info')})

    # Mineirando todos os nomes de empresas e seus respectivos salarios e os organizando em uma lista
    lista_todos_salarios = []
    for empresas, salario in zip(lista_empresas, lista_salarios):
        nome_empresa = empresas.find('a').text
        salario_empresa = int(salario.contents[1].text.replace('R$', '').replace('.',''))
        lista_todos_salarios.append((nome_empresa, salario_empresa))

    # Criando um data frama para uma melhor analise dos dados 
    df_salarios = pd.DataFrame(lista_todos_salarios, columns=['Empresa','Salario'])

    return df_salarios



