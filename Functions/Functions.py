import requests
from bs4 import BeautifulSoup
import telebot
from datetime import datetime, timedelta

cabecalho = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
            'cookie': '_ga=GA1.1.1416259687.1676299727; cookie_consent=1; SLG_G_WPT_TO=pt; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; cf_clearance=gqbQdGT7CQ7lKW7eNGnQb1LS3GHDABcbqwdi0ApYlZA-1677349635-0-160; sid=ms707fr76ddk72bm933t6dtds4; tz=America/Sao_Paulo; _ga_1LTT3CXFKZ=GS1.1.1677349638.3.1.1677349703.0.0.0'
            }

def estatisticasHead(CHAVE_API_TELEGRAM, ID_GRUPO_TELEGRAM, url, linksJogadoresSeparados):

    # Faz a conexao com a url onde se encontra os dados da partida
    headConteudo = requests.get(url, headers=cabecalho)

    # Captura o conteudo da pagina
    headConteudo = headConteudo.content

    # Melhora a leitura do conteudo
    headConteudo = BeautifulSoup(headConteudo, 'html.parser')

    # Verifica se existe um historico de head to head
    if headConteudo.find('div', attrs={'class': 'card-header'}):

        # Pega jogadores, data e horario da proxima partida
        proxPartida = headConteudo.find('h1').text
        # proxPartida = proxPartida.split()

        proxPartida = trataNomeData(proxPartida=proxPartida)

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
{proxPartida}\n\n
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
                enviarMensagem(CHAVE_API_TELEGRAM=CHAVE_API_TELEGRAM, ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, mensagemBotPingPong=mensagem)
                print(mensagem)

            # Condição para mostrar resultados
            elif winJogadorDois >= 70.0 and esta_um < esta_dois:

                mensagem = f"""
🤖POSSÍVEL OPORTUNIDADE!🏓\n
{proxPartida}\n\n
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
                enviarMensagem(CHAVE_API_TELEGRAM=CHAVE_API_TELEGRAM, ID_GRUPO_TELEGRAM=ID_GRUPO_TELEGRAM, mensagemBotPingPong=mensagem)
                print(mensagem)

            else:
                print(f'Partida {proxPartida}, fora dos padrões.\n')
                pass
        else:
            print('Poucos jogos para analise.')

    else:
        print('Partida sem Head to Head!')
        pass


def trataNomeData(proxPartida):

    # Variaveis globais porque são utilizadas para gerar a mensagem
    
    global jogadorUm
    global jogadorDois

    proxPartida = proxPartida
    proxPartida = proxPartida.split()
    horas = 3

    # Tratando nomes dos jogadores (podem ser 3 nomes) | Datas e horarios
    if len(proxPartida) == 7:
        #Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]}'
        jogadorDois = f'{proxPartida[3]} {proxPartida[4]}'

        # Pegando str data e horarios
        dataHorario = f'{proxPartida[5]} {proxPartida[6]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(proxPartida) == 8 and proxPartida[3] == 'vs':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]} {proxPartida[2]}'
        jogadorDois = f'{proxPartida[4]} {proxPartida[5]}'

        # Pegando str data e horarios
        dataHorario = f'{proxPartida[6]} {proxPartida[7]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(proxPartida) == 8 and proxPartida[2] == 'vs':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]}'
        jogadorDois = f'{proxPartida[3]} {proxPartida[4]} {proxPartida[5]}'

        # Pegando str data e horarios
        dataHorario = f'{proxPartida[6]} {proxPartida[7]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} {dataHorario}'

    elif len(proxPartida) == 9 and proxPartida[3] == 'vs':

        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]} {proxPartida[2]}'
        jogadorDois = f'{proxPartida[4]} {proxPartida[5]} {proxPartida[6]}'

        # Pegando str data e horarios
        dataHorario = f'{proxPartida[7]} {proxPartida[8]}'

        # Ajustando data e horario
        dataHorario = datetime.strptime(dataHorario, "%Y-%m-%d %H:%M")
        dataHorario = dataHorario - timedelta(hours=horas)
        dataHorario = dataHorario.strftime("%d/%m/%Y %H:%M")

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} {dataHorario}'


    elif len(proxPartida) == 5 and proxPartida[2] == '0-0':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]}'
        jogadorDois = f'{proxPartida[3]} {proxPartida[4]}'

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} - Partida iniciando agora!'


    elif len(proxPartida) == 7 and proxPartida[3] == '0-0':
        # Encontrando nomes jogadores na lista gerada no split
        jogadorUm = f'{proxPartida[0]} {proxPartida[1]} {proxPartida[2]}'
        jogadorDois = f'{proxPartida[4]} {proxPartida[5]} {proxPartida[6]}'

        # Gerando informação da partida apos tratamento
        return f'{jogadorUm} vs {jogadorDois} - Partida iniciando agora!'


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


def enviarMensagem(CHAVE_API_TELEGRAM, ID_GRUPO_TELEGRAM, mensagemBotPingPong):

    bossBotPingPong = telebot.TeleBot(CHAVE_API_TELEGRAM)
    idGrupo = ID_GRUPO_TELEGRAM
    mensagemBotPingPong = mensagemBotPingPong
    resposta = bossBotPingPong.send_message(idGrupo, mensagemBotPingPong)
    return resposta