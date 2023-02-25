import requests
from bs4 import BeautifulSoup
import time
from Functions.Functions import estatisticasHead


CHAVE_API_TELEGRAM = ""
ID_GRUPO_TELEGRAM = ""
LINK_BASE = "" #Link base para scraping


# Headers para a autenticação / Definir no Functions.py tambem.
cabecalho = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
            'cookie': '_ga=GA1.1.1416259687.1676299727; cookie_consent=1; SLG_G_WPT_TO=pt; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; cf_clearance=gqbQdGT7CQ7lKW7eNGnQb1LS3GHDABcbqwdi0ApYlZA-1677349635-0-160; sid=ms707fr76ddk72bm933t6dtds4; tz=America/Sao_Paulo; _ga_1LTT3CXFKZ=GS1.1.1677349638.3.1.1677349703.0.0.0'
            }

conteudo = requests.get(LINK_BASE+"/cs/table-tennis", headers=cabecalho)


# Pegando conteúdo
conteudo = conteudo.content


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
