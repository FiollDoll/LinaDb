import telebot
import sqlite3

con = sqlite3.Connection("answers.db", check_same_thread=False)
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS answerTotal(
    word TEXT,
    answer TEXT
)""")
con.commit()

bot = telebot.TeleBot("5429800273:AAHv2L6Ihr2L26OnoSDasB1WJOWpfnaE6g8")

newText = False #New word

@bot.message_handler(content_types='text')
def message_reply(message):
    if newText != True:
        talk(message)
    else:
        reg(message)

def talk(message):
    while True:
        global newText
        try:
            word = message.text.lower()
            print(word)
            replacer(word)
            print(word)
            print(cur.execute(f"SELECT word FROM answerTotal WHERE word = '{word}'").fetchone()[0])
            print(word)
            if word == cur.execute(f"SELECT word FROM answerTotal WHERE word = '{word}'").fetchone()[0]:
                bot.send_message(message.chat.id, cur.execute(f"SELECT answer FROM answerTotal WHERE word = '{word}'").fetchone()[0])
                break
            else:
                bot.send_message(message.chat.id, "Как мне отвечать на это?")
                newText = True
                break    
        except:
            bot.send_message(message.chat.id, "Как мне отвечать на это?")
            newText = True
            break    
def reg(message):
    global newText
    global word
    question = message.text
    newText = False
    cur.execute(f"INSERT INTO answerTotal VALUES('{word}', '{question}')")
    con.commit()
def replacer(worder):
    global word
    word = worder.replace(" ", "_")
    word = worder.replace("?", "")
    word = worder.replace("!", "")
    word = worder.replace(",", "")

bot.polling(none_stop = True)
