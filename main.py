import requests
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import telebot
import xmltodict

TOKIN = "7395234686:AAEEOY6CswyYpF1YjUY3cIvZMlMCxZDzcng"
bot = telebot.TeleBot(TOKIN)


def create_inline():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(callback_data="news", text="Get news")
    keyboard.add(button)
    return keyboard


def choose_news():
    news_list = []
    response = requests.get("https://feeds.bbci.co.uk/news/world/rss.xml")  # the rss I am using from BBC news.
    data = xmltodict.parse(response.text)  # Parsing teh xtml rss file to dict
    items = data["rss"]["channel"]["item"]  # collecting all the items/news (data>rss>item)
    print(items)
    for item in items:  # Looking through all the news items
        title = item.get("title")
        description = item.get("description")
        link = item.get("link")
        pub_date = item.get("pubDate")
        date = pub_date[:-12]
        media_thumbnail = item.get("media:thumbnail")
        media_url = media_thumbnail["@url"] if media_thumbnail else None
        news = {"title": title, "description": description, "link": link, "date": date, "image": media_url}
        news_list.append(news)
    random_news = random.choice(news_list)
    return random_news


def create_text(news):
    title = news.get("title")
    description = news.get("description")
    date = news.get("date")
    text = f"<b>{title}</b>\n\n{description}\n\n{date}"
    return text


def check_news(news_list, news):
    pass


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Hello, press the button bellow to get news",
                     reply_markup=create_inline())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "news":
        news = choose_news()  # Choosing random news
        text = create_text(news)  # Creating the text for the message
        #  ---CREATING THE LINK BUTTON---
        keyboard = InlineKeyboardMarkup()
        button_more = InlineKeyboardButton(text="more...", url=news.get("link"))  # More button
        button_news = InlineKeyboardButton(text="NEWS", callback_data="news")  # NEWS button
        keyboard.add(button_more, button_news)  # Adding buttons to keyboard
        # ---SENDING THE MESSAGE---
        bot.send_photo(chat_id=call.message.chat.id, photo=news.get("image"))  # sending image form news
        bot.send_message(chat_id=call.message.chat.id, text=text, parse_mode="HTML", reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
