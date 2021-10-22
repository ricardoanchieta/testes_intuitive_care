from bs4 import BeautifulSoup
import requests
import time

def buscarPadraoTiss():
    html_text = requests.get("https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss")
    soup = BeautifulSoup(html_text.text,'lxml')

    # Procura primeiro container contendo o link da versao mais recente do TISS
    container = soup.find('p', class_ = "callout")
    # Procura e salva nova url dentro do container
    find_url = container.find('a',href=True)
    new_url = find_url['href']

    html_text = requests.get(new_url)
    soup = BeautifulSoup(html_text.text,'lxml')

    #procura tabela que contem as informações do documento a ser baixado
    find_table = soup.find('tbody')
    #acessa a primeira linha da tabela
    line_table = find_table.find('tr')

    #retira dados da tabela
    doc_name = line_table.find_all('td')[0].text
    doc_version = line_table.find_all('td')[1].text

    #pdf a ser baixado
    find_url_pdf = soup.find('a',class_ = "btn btn-primary btn-sm center-block internal-link")
    url_pdf = find_url_pdf['href']

    print(f'''
    Nome do documento:{doc_name}
    Versao do documento:{doc_version}
    ''')

    pdf = requests.get(url_pdf)

    with open('componente_organizacional_'+doc_version+'.pdf', 'wb') as f:
        f.write(pdf.content)
        print("PDF baixado com sucesso!")

if __name__ == "__main__":
    while True:
        buscarPadraoTiss()
        #definir tempo de espera para o programa rodar novamente
        time_wait = 10
        time.sleep(time_wait * 1)

