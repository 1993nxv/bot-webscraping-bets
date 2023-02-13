import requests
from bs4 import BeautifulSoup
import time
import telebot
from datetime import datetime, timedelta

#Ler arquivo keys.txt para pegar keys
CHAVE_API_TELEGRAM = ""
ID_GRUPO_TELEGRAM = ""
LINK_BASE = ""

bossBotPingPong = telebot.TeleBot(CHAVE_API_TELEGRAM)

# Headers para a autenticação.
cabecalho = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117',
            'cookie': '_ga=GA1.1.727667681.1662658727; __gads=ID=64119310dfc77fa7-22fa62d42eb400a5:T=1663292406:RT=1663292406:S=ALNI_Ma7EH0u3xx_54AePPAlLzdyuFQfFA; __gpi=UID=0000096a389932d2:T=1663292406:RT=1663292406:S=ALNI_MZ6Q1Fyz1IAeMntjJNy71fHQ6OQsw; FCNEC=[["AKsRol-0_juf8lAAw_h5JfkqH83RUqyQDjMJcdMGUj2jxUaF_J5xngwAzW8SCWIpUnODPdn6xoDDCZaSw2RAuwoB0MgPhlwesfDmHl-Cadw_JQgaTbcHxSA9A5iKYO-yS3pvydjzBiNfWhR7Ag-EBEW9si7eZ3ezFw=="],null,[]]; __atuvc=1|37,26|38,70|39,10|40; sid=63nktffphrd31h87koqecdtq81; tz=America/Sao_Paulo; cf_chl_2=686153ab5835818; cf_chl_prog=x15; cf_clearance=f14166804562377d001098853c53a3cd54819b1b-1667054291-0-150; _ga_1LTT3CXFKZ=GS1.1.1667054290.163.1.1667054316.0.0.0'
            }


def enviarMensagem(ID_GRUPO_TELEGRAM, mensagemBotPingPong):
    idGrupo = ID_GRUPO_TELEGRAM
    mensagemBotPingPong = mensagemBotPingPong
    resposta = bossBotPingPong.send_message(idGrupo, mensagemBotPingPong)
    return resposta


def estatisticasIndviduais(linksJogadoresSeparados):

    linksJogadoresSeparados = linksJogadoresSeparados

    # Faz a conexao com a url onde se encontra os dados individuais do jogador 1
    ind_read = requests.get(linksJogadoresSeparados[0], headers=cabecalho)

    # Captura o conteudo da pagina
    ind_read = ind_read.content

    # Melhora a leitura do conteudo
    ind_read = BeautifulSoup(ind_read, 'html.parser')

    # Pegando nome do jogador
    nomeJogadorUm = ind_read.find('h1').text
    nomeJogadorUm = nomeJogadorUm.strip()

    # Encontrando linhas vitorias e derrotas
    ind_read = ind_read.findAll('tr')

    # Variaveis de dados jogador um
    numUmPartidas = len(ind_read)
    jogadorUmVitorias = 0
    jogadorUmDerrotas = 0

    # Calculando resultados vitorias e derrotas
    for i in ind_read:
        i = i.find_all_next('td')
        i = i[4].text
        if i == 'W':
             jogadorUmVitorias += 1
        elif i == 'L':
            jogadorUmDerrotas += 1
        elif i == 'D' or i == '-':
            numUmPartidas -= 1

#------------------------------------------------------------------------------------------------------------------

    # Faz a conexao com a url onde se encontra os dados individuais do jogador 2
    ind_read = requests.get(linksJogadoresSeparados[1], headers=cabecalho)

    # Captura o conteudo da pagina
    ind_read = ind_read.content

    # Melhora a leitura do conteudo
    ind_read = BeautifulSoup(ind_read, 'html.parser')

    # Pegando nome do jogador
    nomeJogadorDois = ind_read.find('h1').text
    nomeJogadorDois = nomeJogadorDois.strip()

    # Encontrando linhas vitorias e derrotas
    ind_read = ind_read.findAll('tr')

    # Variaveis de dados jogador dois
    numDoisPartidas = len(ind_read)
    jogadorDoisVitorias = 0
    jogadorDoisDerrotas = 0

    # Calculando resultados vitorias e derrotas
    for i in ind_read:
        i = i.find_all_next('td')
        i = i[4].text
        if i == 'W':
            jogadorDoisVitorias += 1
        elif i == 'L':
            jogadorDoisDerrotas += 1
        elif i == 'D' or i == '-':
            numDoisPartidas -= 1


    resultJogadorUm = f'{nomeJogadorUm} - {numUmPartidas} partidas, ✅ {jogadorUmVitorias} ({(100 / numUmPartidas) * jogadorUmVitorias:.1f}%) | ❌ {jogadorUmDerrotas} ({(100 / numUmPartidas) * jogadorUmDerrotas:.1f}%)'

    resultJogadorDois = f'{nomeJogadorDois} - {numDoisPartidas} partidas, ✅ {jogadorDoisVitorias} ({(100 / numDoisPartidas) * jogadorDoisVitorias:.1f}%) | ❌ {jogadorDoisDerrotas} ({(100 / numDoisPartidas) * jogadorDoisDerrotas:.1f}%)'

    global esta_um
    global esta_dois
    esta_um = (100 / numUmPartidas) * jogadorUmVitorias
    esta_dois = (100 / numDoisPartidas) * jogadorDoisVitorias

    return resultJogadorUm, resultJogadorDois


def trataNomeData(pro_part):

    # Variaveis globais porque são utilizadas para gerar a mensagem
    global prox_part
    global jogadorUm
    global jogadorDois

    pro_part = pro_part
    prox_part = pro_part.split()
    horas = 3

    # Tratando nomes dos jogadores (podem ser 3 nomes) | Datas e horarios
    if len(prox_part) == 7:
        #Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]}'
        jogadorDois = f'{prox_part[3]} {prox_part[4]}'

        # Pegando str data e horarios
        dataHorario = f'{prox_part[5]} {prox_part[6]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(prox_part) == 8 and prox_part[3] == 'vs':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]} {prox_part[2]}'
        jogadorDois = f'{prox_part[4]} {prox_part[5]}'

        # Pegando str data e horarios
        dataHorario = f'{prox_part[6]} {prox_part[7]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(prox_part) == 8 and prox_part[2] == 'vs':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]}'
        jogadorDois = f'{prox_part[3]} {prox_part[4]} {prox_part[5]}'

        # Pegando str data e horarios
        dataHorario = f'{prox_part[6]} {prox_part[7]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} {dataHorario}'

    elif len(prox_part) == 9 and prox_part[3] == 'vs':

        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]} {prox_part[2]}'
        jogadorDois = f'{prox_part[4]} {prox_part[5]} {prox_part[6]}'

        # Pegando str data e horarios
        dataHorario = f'{prox_part[7]} {prox_part[8]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(prox_part) == 5 and prox_part[2] == '0-0':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]}'
        jogadorDois = f'{prox_part[3]} {prox_part[4]}'

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} - Partida iniciando agora!'


    elif len(prox_part) == 7 and prox_part[3] == '0-0':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{prox_part[0]} {prox_part[1]} {prox_part[2]}'
        jogadorDois = f'{prox_part[4]} {prox_part[5]} {prox_part[6]}'

        # Gerando informação da partida apos tratamento
        prox_part = f'{jogadorUm} vs {jogadorDois} - Partida iniciando agora!'


def estatisticasHead(ID_GRUPO_TELEGRAM, url, linksJogadoresSeparados):

    # Faz a conexao com a url onde se encontra os dados da partida
    headConteudo = requests.get(url, headers=cabecalho)

    # Captura o conteudo da pagina
    headConteudo = headConteudo.content

    # Melhora a leitura do conteudo
    headConteudo = BeautifulSoup(headConteudo, 'html.parser')

    # Verifica se existe um historico de head to head
    if headConteudo.find('div', attrs={'class': 'card-header'}):

        # Pega jogadores, data e horario da proxima partida
        pro_part = headConteudo.find('h1').text
        # pro_part = pro_part.split()

        trataNomeData(pro_part=pro_part)

        # Gerando link
        link = f"https://www.bet365.com/?nr=1#/AX/K%5E{jogadorUm.replace(' ', '%20')}%20vs%20{jogadorDois.replace(' ', '%20')}"

        # Busca partidas no historico entre os dois jogadores (head to head)
        headConteudo = headConteudo.find('table', attrs={'class': 'table table-sm'}).findAll('tr')

        # Verifica se o historico head to head é maior que 10 encontros
        if len(headConteudo) >= 6:

            c = 0  # variavel para controle de indices
            contadorUm = 0  # variavel para controle de vitorias jogador 1
            contadorDois = 0  # variavel para controle de vitorias jogador 2
            gamesPum = 0  # variavel para controle venceu ao menos um game

            # Contando numero de partidas head to head
            partidas_hth = len(headConteudo)

            # laço para trabalhar os dados do historico
            for i in headConteudo:

                cont_head = headConteudo[c].findAll('td')

                liga = cont_head[0].text.strip('\n')
                data = cont_head[1].text.strip('\n')
                jogadores = cont_head[2].text.strip('\n')
                worl = cont_head[3].text.strip('\n')
                placar = cont_head[4].text.strip('\n')

                jogadores = jogadores.split()
                jogadores = ' '.join(jogadores)

                # Gera quantidade de vitorias e derrotas
                if worl == 'W':
                    contadorUm += 1
                elif worl == 'L':
                    contadorDois += 1
                elif worl == 'D' or i == '-':
                    partidas_hth -= 1

                # Gera placares
                p = placar.split('-')
                if int(p[0]) > 0 and int(p[1]) > 0:
                    gamesPum += 1

                c += 1

            # Porcentagens
            winJogadorUm = (100 / partidas_hth) * contadorUm
            winJogadorDois = (100 / partidas_hth) * contadorDois

            # Def emoji favorito
            if winJogadorUm > winJogadorDois:
                fav = ['🟢', '🛑']
            elif winJogadorDois > winJogadorUm:
                fav = ['🛑', '🟢']
            else:
                fav = ['🟢', '🟢']

            # Porcetagem games em partidas
            porcAmbosGame = (100 / partidas_hth) * gamesPum

            # Chama Funçao analise individual
            estatisticasIndividuais = estatisticasIndviduais(linksJogadoresSeparados=linksJogadoresSeparados)

            # Condição para mostrar resultados
            if winJogadorUm >= 70.0 and esta_um > esta_dois:

                mensagem = f"""
🤖POSSÍVEL OPORTUNIDADE!🏓\n
{prox_part}\n\n
CONFRONTO DIRETO:{partidas_hth} PARTIDAS
{fav[0]}{jogadorUm} ✅ {contadorUm} Partidas ({winJogadorUm:.1f}%) | ❌ {len(headConteudo) - contadorUm}
{fav[1]}{jogadorDois} ✅ {contadorDois} Partidas ({winJogadorDois:.1f}%) | ❌ {len(headConteudo) - contadorDois}\n\n
➡{porcAmbosGame:.1f}% dos jogos terminaram com o placar maior ou igual a 3-1.
➡{100 - porcAmbosGame:.1f}% dos jogos terminaram com o placar de 3-0\n\n
APROVEITAMENTO INDIVIDUAL:
{estatisticasIndividuais[0]}
{estatisticasIndividuais[1]}
\n\n
Link:
{link}\n(É possivel que a partida ainda não esteja visivel, na Bet365 aguardar 30-40min antes da partida caso aconteça!)
"""
                enviarMensagem(ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, mensagemBotPingPong=mensagem)
                print(mensagem)

            # Condição para mostrar resultados
            elif winJogadorDois >= 70.0 and esta_um < esta_dois:

                mensagem = f"""
🤖POSSÍVEL OPORTUNIDADE!🏓\n
{prox_part}\n\n
CONFRONTO DIRETO:{partidas_hth} PARTIDAS
{fav[0]}{jogadorUm} ✅ {contadorUm} Partidas ({winJogadorUm:.1f}%) | ❌ {len(headConteudo) - contadorUm}
{fav[1]}{jogadorDois} ✅ {contadorDois} Partidas ({winJogadorDois:.1f}%) | ❌ {len(headConteudo) - contadorDois}\n\n
➡{porcAmbosGame:.1f}% dos jogos terminaram com o placar maior ou igual a 3-1.
➡{100 - porcAmbosGame:.1f}% dos jogos terminaram com o placar de 3-0\n\n
APROVEITAMENTO INDIVIDUAL:
{estatisticasIndividuais[0]}
{estatisticasIndividuais[1]}
\n\n
Link:
{link}\n(É possivel que a partida ainda não esteja visivel, na Bet365 aguardar 30-40min antes da partida caso aconteça!)
                    """
                enviarMensagem(ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, mensagemBotPingPong=mensagem)
                print(mensagem)

            else:
                print(f'Partida {prox_part}, fora dos padrões.\n')
                pass
        else:
            print('Poucos jogos para analise.')

    else:
        print('Partida sem Head to Head!')
        pass


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
    estatisticasHead(ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, url=url, linksJogadoresSeparados=linksJogadoresSeparados)

    # Controle para links dos jogadores individuais
    controle += 1

    time.sleep(30)
