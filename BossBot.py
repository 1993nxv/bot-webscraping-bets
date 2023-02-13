import telebot

CHAVE_API = ""
bossBot1 = telebot.TeleBot(CHAVE_API)


def verificarMen(mensagem):
    if mensagem:
        return True

@bossBot1.message_handler(func=verificarMen)
def responder(mensagem):
    texto = """
Olá, aqui é o 🏓 Bot Ping Pong Boss! 

🤖 Envio sinais com oportunidades no mercado de Tênis de Mesa da Bet365.
Diariamente são mais 1400 partidas e muitas oportunidade de 🟢💸

Ensino também as estratégias a serem utilizadas para aproveitar ao máximo os sinais!
https://bit.ly/pingpongboss

🏓🤖 Sinais PP Boss - Pre-Live
Para assinar por 30 dias por apenas R$39,99 
basta mandar um start para:
https://t.me/Gerente_boss_pre_bot

            """
    bossBot1.reply_to(mensagem, texto)

try:
    bossBot1.polling()
except:
    bossBot1.polling()