import telebot
from telebot import types
from django.conf import settings
from .models import User, Clients
import openpyxl
import os

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = telebot.TeleBot(settings.TOKEN_BOT)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_name = message.from_user.username

    client, created = Clients.objects.get_or_create(user_id=user_id)
    if created:
        client.first_name = user_first_name
        client.last_name = user_last_name
        client.username = user_name
        client.save()

    welcome_message = "Hello"
    bot.reply_to(message, welcome_message)


@bot.message_handler(commands=['godmode', 'help'])
def send_god_mode(message):
    telegram_name = f"@{message.from_user.username}"
    try:
        user = User.objects.get(telegram_name=telegram_name, is_staff=True)
        if user.telegram_name is not None and user.is_staff:
            buttons = ['EXCEL 📝', 'Список пользователей 👤', 'Option 3']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(buttons[0], buttons[1], buttons[2])
            bot.send_message(message.chat.id, "You are my God", reply_markup=keyboard)
    except User.DoesNotExist:
        bot.send_message(message.chat.id, "You are not my God")


@bot.message_handler(func=lambda message: message.text == 'EXCEL 📝')
def handle_excel_request(message):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        current_datetime = result.strftime("%Y%m%d_%H%M")
        excel_file_path = f'report_{current_datetime}.xlsx'
        create_excel(excel_file_path)

        with open(excel_file_path, 'rb') as excel_file:
            bot.send_document(c.message.chat.id, excel_file, caption="Here is the Excel file")
        os.remove(excel_file_path)

        bot.edit_message_text(f"You selected {result}", c.message.chat.id, c.message.message_id)


def create_excel(file_path):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet['A1'] = 'User ID'
    worksheet['B1'] = 'First Name'
    worksheet['C1'] = 'Last Name'
    worksheet['D1'] = 'Username'
    clients_data = Clients.objects.all().values_list('user_id', 'first_name', 'last_name', 'username')
    for row_num, client_data in enumerate(clients_data, start=2):
        for col_num, value in enumerate(client_data, start=1):
            worksheet.cell(row=row_num, column=col_num, value=value)
    workbook.save(file_path)


@bot.message_handler(func=lambda message: message.text == 'Список пользователей 👤')
def handle_option_2(message):
    clients_data = Clients.objects.all()
    if clients_data:
        client_list_message = "Список пользователей:\n"
        for client in clients_data:
            client_list_message += f"User ID: {client.user_id}, First Name: {client.first_name}, Last Name: {client.last_name}, Username: {client.username}\n"
        bot.send_message(message.chat.id, client_list_message)
    else:
        bot.send_message(message.chat.id, "No Clients found.")


if __name__ == "__main__":
    bot.polling()
