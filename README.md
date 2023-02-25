# bot-webscraping-bets

<h2>Descrição</h2>
<p>O projeto consiste em um script que consulta informações das próximas 100 partidas de ping pong, processa os dados e envia estatísticas de cada partida considerando os últimos 30 encontros.</p>
<h2>Lógica</h2>
<p>O envio dos sinais é definido por cálculos feitos com base no histórico dos últimos 30 confrontos diretos entre os jogadores, definindo se um jogador é realmente favorito para vencer a partida.</p>
<h3>Estatísticas enviadas nos sinais:</h3>
<ul>
<li>Vitórias e derrotas de cada jogador (confrontos diretos) + porcentagens</li>
<li>Porcentagens dos placares</li>
<li>Aproveitamento individual de cada jogador + porcentagens</li>
</ul>

<h2>Visualização no Terminal</h2>
<img src="https://github.com/1993nxv/bot-webscraping-bets/blob/main/img/terminal.png"></img>

<h2>Sinal enviado no Grupo do Telegram</h2>
<img src="https://github.com/1993nxv/bot-webscraping-bets/blob/main/img/telegram.png"></img>

<h3>Projeto utiliza:</h3>
<ul>
<li>Python 3.10</li>
<li>Requests 3.0.1</li>
<li>BeautifulSoup 4.11.2</li>
<li>Telebot 4.10.0</li>
</ul>

