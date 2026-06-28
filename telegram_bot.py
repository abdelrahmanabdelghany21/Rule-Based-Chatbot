import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv("token")

if not TELEGRAM_TOKEN:
    raise ValueError("Error: TELEGRAM_TOKEN not found! Please create a .env file.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
FASTAPI_URL = "http://127.0.0.1:8000/chat"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ **Welcome to ICT HUB EGYPT!** ✨\n\n"
        "We are a leading provider of digital solutions, committed to driving innovation "
        "and empowering the next generation of tech professionals through real-world experience.\n\n"
        "💡 **You can ask me about:**\n\n"
        "* 📍 **Location**\n"
        "* 📋 **Internship Details**\n"
        "* 🤖 **AI Internship Details**\n"
        "* 🔒 **Cyber Security Internship Details**\n"
        "* 🌐 **Web Development Internship Details**\n"
        "* 📊 **Data Analysis Internship Details**\n"
        "* 📱 **Flutter Internship Details**\n"
        "* 📦 **Supply Chain Internship Details**\n\n"
        "Feel free to type any of the topics above to get started and I will assist you instantly!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    print("[Telegram] New user received and pressed /start")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    print(f"\n[Telegram] New message received: '{user_text}'")
    
    try:
        print(f"[API] Sending message to API at URL: {FASTAPI_URL} ...")
        response = requests.post(FASTAPI_URL, json={"user_message": user_text}, timeout=10)
        
        if response.status_code == 200:
            api_data = response.json()
            bot_reply = api_data["bot_response"]
            predicted_cat = api_data["predicted_category"]
            
            print(f"[FastAPI] Prediction success! Category: '{predicted_cat}'")
            print(f"[Telegram] Sending response back to user...")
            
            bot.reply_to(message, bot_reply)
        else:
            print(f"[FastAPI] Server responded with an error code: {response.status_code}")
            bot.reply_to(message, "Sorry, I encountered an error processing your request internally.")
            
    except requests.exceptions.ConnectionError:
        print("[Connection Error] Failed to connect to FastAPI. Make sure the uvicorn server is running!")
        bot.reply_to(message, "Sorry, the smart server is currently out of service (FastAPI is not running).")
        
    except Exception as e:
        print(f"[Unexpected Error]: {str(e)}")
        bot.reply_to(message, "Sorry, an unexpected error occurred while processing your message.")

if __name__ == "__main__":
    print("=============================================")
    print("Telegram bot is now running and ready to receive messages...")
    print("Make sure the uvicorn server is running in another terminal window.")
    print("=============================================")
    bot.infinity_polling()