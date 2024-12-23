import telebot
import os
import google.generativeai as gemini
from gtts import gTTS

from dotenv import load_dotenv

load_dotenv()

teleAPI = os.getenv("TELE_API")
geminiAPI = os.getenv("GEMINI_API")
identityBOT = os.getenv("IDENTITYBOT")
deepgram_api = os.getenv("DEEPGRAM_API")

client = gemini.GenerativeModel('gemini-1.5-flash-002')
gemini.configure(api_key=geminiAPI)

botTele = telebot.TeleBot(token=teleAPI)


@botTele.message_handler(func=lambda msg : True)
def sendMessage(message):
    identity = identityBOT #add identity
    response = client.generate_content(identity + message.text) #generate output for gemini
    result = response.text.removeprefix("*")
    out = gTTS(result , lang='id') #generate text to speech
    out.save('output.mp3') #save the voice 
    with open("output.mp3" ,"rb") as voice:
        botTele.send_voice(message.chat.id , voice)

def main():
    botTele.polling()



if __name__ == '__main__':
    main()