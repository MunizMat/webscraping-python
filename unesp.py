from bs4 import BeautifulSoup
import requests
from datetime import datetime
materia = input("Escolha uma matéria: ")
url = f"https://www.stoodi.com.br/exercicios/{materia}/"
req = requests.get(url)
doc = BeautifulSoup(req.text, 'html.parser')
sec = doc.find_all(['li'], class_='exercise')
assuntos = {}
for x in sec:
    assunto = x.string
    pag = x.a.get('href')

    assuntos[assunto] = f'https://www.stoodi.com.br{pag}'

print(assuntos.keys())
asssunto_selecionado = input('Insira o assunto desejado: ')
start_time = datetime.now()
url_questoes = assuntos[asssunto_selecionado]
req2 = requests.get(url_questoes)
doc2 = BeautifulSoup(req2.text, 'html.parser')
sec2 = doc2.find(['nav'], class_='pagination--secondary')
int_list = []
for x in sec2:
    for y in x:
        int_list.append(y.a)
num_pages = int(int_list[-2].string)
urls = []
for page in range(1, num_pages + 1):
    url_page = f'{url_questoes}?page={page}'
    req_page = requests.get(url_page)
    doc_page = BeautifulSoup(req_page.text, 'html.parser')
    ol = doc_page.ol
    lis = ol.contents
    for li in lis:
        for conts in li.contents:
            vestibular = conts.h4.string
            if 'UNESP' in vestibular:
                link = conts.get('href')
                link2 = f'https://www.stoodi.com.br/{link}'
                urls.append(link2)



for pagina in urls:
    url3 = pagina
    req3 = requests.get(url3)
    doc3 = BeautifulSoup(req3.text, 'html.parser')
    sec3 = doc3.find_all(['h3'], class_='c-exercise__institution')
    banca = sec3[0].string
    print(banca)
    texto = doc3.find_all(['div'], class_='c-exercise__text')
    texto2 = texto[0].text
    print(texto2)
    alt = doc3.find_all(['ul'], class_='c-q-list c-exercise__alternatives')
    images = doc3.find_all(['img'], alt='')
    options = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    i = 1
    for alternativas in alt:
        for li in alternativas:
            print(f'{options[i]}){li.text}')
            i += 1
    if len(images) != 0:
        for x in images:
            print(x.get('src'))

end_time = datetime.now()
print(end_time - start_time)
print(len(urls))
