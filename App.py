import requests
from bs4 import BeautifulSoup
import time
from Functions.Functions import estatisticasHead


CHAVE_API_TELEGRAM = ""
ID_GRUPO_TELEGRAM = ""
LINK_BASE = "" #Link base para scraping


# Headers para a autenticação / Definir no Functions.py tambem.
cabecalho = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117',
            'cookie': '_ga=GA1.1.727667681.1662658727; __gads=ID=64119310dfc77fa7-22fa62d42eb400a5:T=1663292406:RT=1663292406:S=ALNI_Ma7EH0u3xx_54AePPAlLzdyuFQfFA; __gpi=UID=0000096a389932d2:T=1663292406:RT=1663292406:S=ALNI_MZ6Q1Fyz1IAeMntjJNy71fHQ6OQsw; FCNEC=[["AKsRol-0_juf8lAAw_h5JfkqH83RUqyQDjMJcdMGUj2jxUaF_J5xngwAzW8SCWIpUnODPdn6xoDDCZaSw2RAuwoB0MgPhlwesfDmHl-Cadw_JQgaTbcHxSA9A5iKYO-yS3pvydjzBiNfWhR7Ag-EBEW9si7eZ3ezFw=="],null,[]]; __atuvc=1|37,26|38,70|39,10|40; sid=63nktffphrd31h87koqecdtq81; tz=America/Sao_Paulo; cf_chl_2=686153ab5835818; cf_chl_prog=x15; cf_clearance=f14166804562377d001098853c53a3cd54819b1b-1667054291-0-150; _ga_1LTT3CXFKZ=GS1.1.1667054290.163.1.1667054316.0.0.0'
            }


respost = requests.get(LINK_BASE+"/cs/table-tennis", headers=cabecalho)


# Pegando conteúdo
conteudo = respost.content


# Melhorando visualização do retorno
conteudo = BeautifulSoup(conteudo, 'html.parser')


# Encontrando elemento
proxPartidas = conteudo.findAll('tr')


# Lista para links head to head
linksEncontrosHeadToHead = []
# Lista para links historico individual de cada jogador
linksJogadores = []


for c in proxPartidas:
    # Capturando links das proximas partidas e historico jogadores
    links = c.find_all_next('a')

    # Pegando links com .get \ Unindo os dois links dos jogadores separado * para split posterior
    linksJogadores.append(LINK_BASE+links[1].get('href').replace('/t/', '/te/')+'*'+LINK_BASE+links[2].get('href').replace('/t/', '/te/'))

    # Pegando link manualmente
    d = str(links[3])
    repl = d.replace('<a href="', '')
    repl = repl.replace('">View</a>', '')
    repl = repl.replace('/r/', '/')
    linksEncontrosHeadToHead.append(LINK_BASE+'/rh2h'+repl)


controle = 0  # Variavel de controle links jogadores get

# Repetiçao para analisar partidas
for partida in linksEncontrosHeadToHead:

    # Link partida / links jogadores []
    url = partida
    linksJogadoresSeparados = linksJogadores[controle].split('*')

    # Printa urls sendo analisadas no momento
    print('\n', partida)
    print(linksJogadoresSeparados, '\n')
    print(f'Contador: {controle}')

    # Chamando função para analise partida
    estatisticasHead(CHAVE_API_TELEGRAM=CHAVE_API_TELEGRAM, ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, url=url, linksJogadoresSeparados=linksJogadoresSeparados)

    # Controle para links dos jogadores individuais
    controle += 1

    time.sleep(30)
