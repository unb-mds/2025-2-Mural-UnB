import requests # baixa o HTML
from bs4 import BeautifulSoup # organiza o HTML em python
import urllib.parse #

url_alvo = "" # o link do laboratório

print("Acessando a página: {url_alvo}...")
try:
    response = requests.get(url_alvo) #response = a caixa com tudo que veio da url, pode ser mais ou menos que o HTML puro
    response.raise_for_status() # deu certo ou não?
    print("Página acessada com sucesso!")
    soup = BeautifulSoup(response.content, 'html.parser') # o .content é o conteúdo bruto HTML, html.parser é o tradutor, o BeautifulSoup organiza de forma legível em python
except requests.exceptions.RequestException as motivo: # categoria de todos os erros que podem vir na biblioteca requests, guarde a info no 'motivo'
    print(f"Erro ao acessar a página: {motivo}")
    exit()

