from matplotlib.pyplot import text
from helpers import read_json
from telebot import types
import telebot
from config import TOKEN

questions = ["do you like pizza", "do you like swim in the sea", "do you like to watch movies"]
questions_index = 0 
answers = []
state  = read_json("state.json")
state_index = "hello" 
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["link"])
def link_handler(message):
    mark_up=types.InlineKeyboardMarkup()
    button=types.InlineKeyboardButton(text="google", url="https://google.com")
    mark_up.add(button)
    bot.send_message(message.chat.id, "find", reply_markup=mark_up)

@bot.message_handler(commands=["switch"])
def switch_handler(message):
    markup=types.InlineKeyboardMarkup()
    button=types.InlineKeyboardButton(text="switch", switch_inline_query="telegram")
    markup.add(button)
    bot.send_message(message.chat.id, text="choose chat", reply_markup=markup)

def gen_markup(text_left, text_right):
    markup=types.InlineKeyboardMarkup()
    left_button=types.InlineKeyboardButton(text=text_left, callback_data="left")
    right_button=types.InlineKeyboardButton(text=text_right, callback_data="right")
    markup.row_width=2
    markup.add(left_button, right_button)
    return markup

def gen_markup_array(array):
    markup=types.InlineKeyboardMarkup()
    
    for button in array:
        button=types.InlineKeyboardButton(text=button["text"], callback_data = button["data"])
        markup.add(button) 

    markup.row_width=2
    return markup
    
@bot.message_handler(content_types=["text"])
def state_handler(message):
    global state_index

    markup=gen_markup("text_yes", "text_no")
    if state[state_index]["InlineKeyboard"] == "not":
        markup=""
    else:
        markup = gen_markup_array(state[state_index]["InlineKeyboard"])

    bot.send_message(message.chat.id, text=state[state_index]["message"] , reply_markup=markup)
    if state_index == "hello":
        state_index = "age"
    elif state_index == "age":
        state_index = "ready"



@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    global state_index
    print(state_index, call)
    if state_index == "ready": 
        if call.data == "yes": 
            state_index = "questions_1"
        elif call.data == "no":
            state_index = "pause"

    elif state_index == "pause":
        state_index = "questions_1"

    elif state_index == "questions_1":
        state_index = "recorded"

    elif state_index == "recorded":
        if call.data == "another_one_state":
            state_index = "questions_1"
    
        else:
            bot.send_message(call.message.chat.id, text = "Come when you're in a good mood!")




    markup=gen_markup("text_yes", "text_no")
    if state[state_index]["InlineKeyboard"] == "not":
        markup=""
    else:
        markup = gen_markup_array(state[state_index]["InlineKeyboard"])

    bot.send_message(call.message.chat.id, text=state[state_index]["message"] , reply_markup=markup)

# @bot.callback_query_handler(func = lambda call:call.data == "left")
# def left_handler(call):
#     global questions_index
#     bot.answer_callback_query(call.id, show_alert=True, text="left")
#     answers.append("yes")
#     questions_index += 1
#     print(answers)
#     bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = questions[questions_index], reply_markup=gen_markup("yes", "no"))

# @bot.callback_query_handler(func = lambda call:call.data == "right")
# def right_handler(call):
#     global questions_index
#     bot.answer_callback_query(call.id, show_alert=True, text="right")
#     answers.append("no")
#     questions_index += 1
#     print(answers)
#     bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = questions[questions_index], reply_markup=gen_markup("yes", "no"))

# @bot.message_handler(func=lambda message: message.text  == "select")
# def lambda_handler(message):
#     bot.send_message(message.chat.id, text = questions[questions_index], reply_markup=gen_markup("yes", "no"))


@bot.message_handler(content_types="text")
def message(message):
    bot.send_message(message.chat.id, "hello")



bot.infinity_polling()