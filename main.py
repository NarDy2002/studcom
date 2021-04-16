import telebot
from telebot import types

import json

import db
import configure

bot = telebot.TeleBot(configure.config["token"])

id1 = ""
firstname = ""
lastname = ""
university = ""
faculty = ""
category = ""
skills = ""
portfolio = ""

edit_type = ""

check = False


@bot.message_handler(commands=['start'])
def any_msg(message):
    global id1
    id1 = str(message.from_user.id)
    users = db.get_db(configure.config["db"]["users"])

    if id1 in list(users.keys()):
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        button_1 = types.InlineKeyboardButton(text="Join Group", callback_data="join_group")
        button_2 = types.InlineKeyboardButton(text="Create Group", callback_data="create_group")
        button_3 = types.InlineKeyboardButton(text="My projects", callback_data="my_projects")
        button_4 = types.InlineKeyboardButton(text="Edit Profile", callback_data="edit_profile")
        button_5 = types.InlineKeyboardButton(text="Info", callback_data="info")
        keyboardmain.add(button_1, button_2, button_3, button_4, button_5)
        bot.send_message(message.chat.id, text = f"Firstname: {users[id1]['firstname']}\nLastname: {users[id1]['lastname']}\nUniversity: {users[id1]['university']}\nFaculty: {users[id1]['faculty']}\nCategory: {users[id1]['category']}\nSkills: {users[id1]['skills']}\nPortfolio: {users[id1]['portfolio']}\n", reply_markup=keyboardmain)

    else:
        keyboardmain = types.InlineKeyboardMarkup(row_width=1)
        button_1 = types.InlineKeyboardButton(text="Sign up", callback_data="sign_up")
        button_2 = types.InlineKeyboardButton(text="Help", callback_data="help")
        button_3 = types.InlineKeyboardButton(text="Contact us", callback_data="contact_us")
        keyboardmain.add(button_1, button_2, button_3)
        bot.send_message(message.chat.id,"Hi there!\nI am a bot 🤖 that will help you find like-minded people, join a project or create your own.",reply_markup=keyboardmain)


def message_lastname(message):
    global firstname
    firstname = message.text
    bot.send_message(message.chat.id, "Input lastname")
    bot.register_next_step_handler(message, message_faculty)


def message_university(message):
    global lastname
    lastname = message.text
    bot.send_message(message.chat.id, "Input university")
    bot.register_next_step_handler(message, message_faculty)

def message_faculty(message):
    global university
    university = message.text
    bot.send_message(message.chat.id, "Input faculty")
    bot.register_next_step_handler(message, message_category)

def message_category(message):
    global faculty
    faculty = message.text
    bot.send_message(message.chat.id, "Input category")
    bot.register_next_step_handler(message, message_skills)

def message_skills(message):
    global category
    category = message.text
    bot.send_message(message.chat.id, "Input skills")
    bot.register_next_step_handler(message, message_portfolio)

def message_portfolio(message):
    global skills
    skills = message.text
    bot.send_message(message.chat.id, "Input portfolio")
    bot.register_next_step_handler(message, message_result)

def message_result(message):
    global portfolio
    portfolio = message.text

    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text="Done", callback_data="menu")
    button_2 = types.InlineKeyboardButton(text="Cancel", callback_data="welcome")
    keyboardmain.add(button_1, button_2)
    bot.send_message(message.chat.id, f"Firstname: {firstname}\nLastname: {lastname}\nUniversity: {university}\nFaculty: {faculty}\nCategory: {category}\nSkills: {skills}\nPortfolio: {portfolio}\n",reply_markup=keyboardmain)
    bot.register_next_step_handler(message, menu)

def menu(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text="Join Group", callback_data="join_group")
    button_2 = types.InlineKeyboardButton(text="Create Group", callback_data="create_group")
    button_3 = types.InlineKeyboardButton(text="My projects", callback_data="my_projects")
    button_4 = types.InlineKeyboardButton(text="Edit Profile", callback_data="edit_profile")
    button_5 = types.InlineKeyboardButton(text="Info", callback_data="info")
    keyboardmain.add(button_1, button_2, button_3, button_4, button_5)
    bot.send_message(message.chat.id,"Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3",reply_markup=keyboardmain)


def edit_profile_back(message):
    global edit_type

    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text="Edit", callback_data="e_" + edit_type)
    button_2 = types.InlineKeyboardButton(text="Done", callback_data="edit_profile")
    button_3 = types.InlineKeyboardButton(text="Cancel", callback_data="edit_profile")
    keyboardmain.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id, f"Correct {edit_type} {message.text}?",reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):

    if call.data[:2] == "e_":
        global edit_type
        edit_type = call.data[2:]
        # bot.send_message(chat_id=call.message.chat.id, text=f"Enter new {edit_type}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Enter new {edit_type}")
        bot.register_next_step_handler(call.message, edit_profile_back)

    if call.data == "sign_up":
        bot.send_message(call.message.chat.id, "Input firstname")
        bot.register_next_step_handler(call.message, message_lastname)

    if call.data == "welcome":
        keyboardmain = types.InlineKeyboardMarkup(row_width=1)
        button_1 = types.InlineKeyboardButton(text="Sign up", callback_data="sign_up")
        button_2 = types.InlineKeyboardButton(text="Help", callback_data="help")
        button_3 = types.InlineKeyboardButton(text="Contact us", callback_data="contact_us")
        keyboardmain.add(button_1, button_2, button_3)
        bot.edit_message_text(call.message.chat.id, call.message.message_id, "Hi there!\nI am a bot 🤖 that will help you find like-minded people, join a project or create your own.",reply_markup=keyboardmain)

    if call.data == "menu":
        global id1
        db.push_db(configure.config["db"]["users"], {
            id1: {
                "firstname": firstname,
                "lastname": lastname,
                "university": university,
                "faculty": faculty,
                "category": category,
                "skills": skills,
                "portfolio": portfolio
            }
        })

        print(db.get_db(configure.config["db"]["users"]))

        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        button_1 = types.InlineKeyboardButton(text="Join Group", callback_data="join_group")
        button_2 = types.InlineKeyboardButton(text="Create Group", callback_data="create_group")
        button_3 = types.InlineKeyboardButton(text="My projects", callback_data="my_projects")
        button_4 = types.InlineKeyboardButton(text="Edit Profile", callback_data="edit_profile")
        button_5 = types.InlineKeyboardButton(text="Info", callback_data="info")
        keyboardmain.add(button_1, button_2, button_3, button_4, button_5)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3", reply_markup=keyboardmain)

    if call.data == "edit_profile":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button_1 = types.InlineKeyboardButton(text="Name", callback_data="e_name")
        button_2 = types.InlineKeyboardButton(text="About myself", callback_data="e_am")
        button_3 = types.InlineKeyboardButton(text="Category", callback_data="e_category")
        button_4 = types.InlineKeyboardButton(text="Portfolio", callback_data="e_portfolio")
        backbutton = types.InlineKeyboardButton(text="Back to menu", callback_data="menu")
        keyboard.add(button_1,button_2,button_3,button_4,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3", reply_markup=keyboard)

    if call.data == "my_projects":
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="STUDCOM", callback_data="studcom")
        backbutton = types.InlineKeyboardButton(text="Back", callback_data="menu")
        keyboard.add(button_1,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3", reply_markup=keyboard)

    if call.data == "info":
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="Help", callback_data="help")
        button_2 = types.InlineKeyboardButton(text="Contact us", callback_data="contact_us")
        backbutton = types.InlineKeyboardButton(text="Back", callback_data="menu")
        keyboard.add(button_1,button_2, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3", reply_markup=keyboard)

    if call.data == "join_group":
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="View offers", callback_data="view_offers")
        button_2 = types.InlineKeyboardButton(text="Find by kw", callback_data="fbk")
        backbutton = types.InlineKeyboardButton(text="Back", callback_data="menu")
        keyboard.add(button_1,button_2, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: Nazarii\nCategory: programming\nRating: 99.1%\nPortfolio: https://telegra.ph/haj-04-13-3", reply_markup=keyboard)

    if call.data == "view_offers":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button_1 = types.InlineKeyboardButton(text="Join", callback_data="join")
        button_2 = types.InlineKeyboardButton(text="Next", callback_data="next")
        backbutton = types.InlineKeyboardButton(text="Cancel", callback_data="join_group")
        keyboard.add(button_1,button_2, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Name: STUDCOM\nTheme: telegram bot for student communication\nRequired skills: python, PyTelegramBotAPI, json\nSquad: 3/5\nTime limit: 23:59 15.04\nhttps://telegra.ph/info-about-project-04-14 ", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)
