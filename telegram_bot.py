#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram бот-ассистент продавец для "Производственной группы Кайман"
"""

import telebot
import json
import base64
import time
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

# Инициализация бота
BOT_TOKEN = "8303280861:AAH6Z7yrqnzD-S1NfhZUOcFwizK4gPjfksc"
bot = telebot.TeleBot(BOT_TOKEN)

class TelegramSalesAssistant:
    def __init__(self):
        """
        Инициализация Telegram ассистента-продавца
        """
        # База данных товаров
        self.products_db = {
            "сетка_рабица": {
                "name": "Сетка рабица оцинкованная",
                "prices": {
                    "45x45_1.6": {"price": 1100, "description": "45×45 мм (1,6 мм) - 1,5×10 м"},
                    "50x50_1.6": {"price": 1130, "description": "50×50 мм (1,6 мм) - 1,5×10 м"},
                    "60x60_2.0": {"price": 1365, "description": "60×60 мм (2,0 мм) - 1,5×10 м"}
                },
                "description": "Универсальный материал для ограждений, вольеров, армирования"
            },
            "колючая_проволока": {
                "name": "Колючая проволока ГОСТ 285-69",
                "price": 5460,
                "description": "Бухта 400 метров (35 кг), диаметр основы 2,8 мм, шипа 2 мм"
            },
            "сбб_акл": {
                "name": "Спиральный барьер безопасности СББ АКЛ",
                "description": "Диаметр 300-1500 мм, длина 4-20 м, витков 15-105",
                "features": ["Высокий уровень защиты", "Усиленная конструкция", "Универсальность применения"]
            },
            "пбб_акл": {
                "name": "Плоский барьер безопасности ПББ АКЛ",
                "description": "Плоские витки, скрепленные скобами, срок службы до 25 лет",
                "features": ["Максимальная надежность", "Компактность", "Простота монтажа"]
            },
            "пклз_акация": {
                "name": "Плоское колючее ленточное заграждение ПКЛЗ 'Акация'",
                "description": "Сетчатое полотно из армированной колючей ленты",
                "features": ["Малозаметность", "Высокий останавливающий эффект", "Устойчивость к коррозии"]
            }
        }
        
        # Акции и скидки
        self.promotions = {
            "скидка_объем": "Скидки от 5% при заказе от 5 рулонов",
            "бесплатная_доставка": "Бесплатная доставка при заказе от 10000₽",
            "гарантия": "Гарантия качества на всю продукцию"
        }
        
        # Контакты компании
        self.company_contacts = {
            "phone": "+7 (910) 598-29-58",
            "address": "г. Людиново, ул. Пролетарская 145",
            "email": "kaiman40@mail.ru",
            "order_email": "grazm47@yandex.ru"
        }
        
        # Хранилище заявок
        self.orders = {}
        
        # Состояния пользователей
        self.user_states = {}

    def get_main_menu(self):
        """
        Создает главное меню бота
        """
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            telebot.types.KeyboardButton("📦 Каталог товаров"),
            telebot.types.KeyboardButton("💰 Акции и цены"),
            telebot.types.KeyboardButton("📞 Контакты"),
            telebot.types.KeyboardButton("🛒 Сделать заказ"),
            telebot.types.KeyboardButton("❓ Помощь")
        )
        return markup

    def get_catalog_menu(self):
        """
        Создает меню каталога
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton("🔗 Сетка рабица", callback_data="product_сетка_рабица"),
            telebot.types.InlineKeyboardButton("🦔 Колючая проволока", callback_data="product_колючая_проволока"),
            telebot.types.InlineKeyboardButton("🌀 СББ АКЛ", callback_data="product_сбб_акл"),
            telebot.types.InlineKeyboardButton("📏 ПББ АКЛ", callback_data="product_пбб_акл"),
            telebot.types.InlineKeyboardButton("🌿 ПКЛЗ 'Акация'", callback_data="product_пклз_акация")
        )
        return markup

    def get_order_menu(self):
        """
        Создает меню заказа
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("📞 Оставить контакты", callback_data="order_contacts"),
            telebot.types.InlineKeyboardButton("📋 Рассчитать стоимость", callback_data="order_calculate"),
            telebot.types.InlineKeyboardButton("🚚 Узнать о доставке", callback_data="order_delivery")
        )
        return markup

    def show_welcome_message(self, chat_id):
        """
        Показывает приветственное сообщение
        """
        welcome_text = """
🤖 Добро пожаловать в "Производственную группу Кайман"!

Я Добрыня, ваш персональный консультант по колючим заграждениям и сетке рабице.

🔧 Что я умею:
• Помогать с выбором товаров
• Рассчитывать стоимость
• Принимать заявки
• Отвечать на вопросы

Выберите нужный раздел в меню ниже 👇
        """
        bot.send_message(chat_id, welcome_text, reply_markup=self.get_main_menu())

    def show_catalog(self, chat_id):
        """
        Показывает каталог товаров
        """
        catalog_text = """
📦 КАТАЛОГ ТОВАРОВ

Выберите интересующий вас товар:
        """
        bot.send_message(chat_id, catalog_text, reply_markup=self.get_catalog_menu())

    def show_product_info(self, chat_id, product_key):
        """
        Показывает информацию о товаре
        """
        if product_key not in self.products_db:
            bot.send_message(chat_id, "❌ Товар не найден")
            return
        
        product = self.products_db[product_key]
        
        if product_key == "сетка_рабица":
            text = f"""
🔗 {product['name']}

{product['description']}

💰 Цены за рулон 1,5×10 м:
• 45×45 мм (1,6 мм): {product['prices']['45x45_1.6']['price']}₽
• 50×50 мм (1,6 мм): {product['prices']['50x50_1.6']['price']}₽  
• 60×60 мм (2,0 мм): {product['prices']['60x60_2.0']['price']}₽

📞 Для заказа оставьте контакты!
            """
        elif product_key == "колючая_проволока":
            text = f"""
🦔 {product['name']}

{product['description']}

💰 Цена: {product['price']}₽ за бухту

📞 Для заказа оставьте контакты!
            """
        else:
            text = f"""
{product['name']}

{product['description']}

✨ Преимущества:
"""
            for feature in product['features']:
                text += f"• {feature}\n"
            text += "\n📞 Для заказа оставьте контакты!"
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🛒 Заказать", callback_data=f"order_{product_key}"),
            telebot.types.InlineKeyboardButton("📞 Контакты", callback_data="show_contacts"),
            telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_catalog")
        )
        
        bot.send_message(chat_id, text, reply_markup=markup)

    def show_promotions(self, chat_id):
        """
        Показывает акции и цены
        """
        text = """
💰 АКЦИИ И СПЕЦИАЛЬНЫЕ ПРЕДЛОЖЕНИЯ

🎉 Текущие акции:
"""
        for promo_id, description in self.promotions.items():
            text += f"• {description}\n"
        
        text += f"""

📞 Для получения персональных предложений оставьте контакты!

💡 Скидки зависят от объема заказа:
• От 5 рулонов - скидка 5%
• От 10 рулонов - скидка 10%
• Крупные заказы - индивидуальные условия
        """
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("📞 Оставить контакты", callback_data="order_contacts"),
            telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
        )
        
        bot.send_message(chat_id, text, reply_markup=markup)

    def show_contacts(self, chat_id):
        """
        Показывает контакты компании
        """
        text = f"""
📞 КОНТАКТЫ КОМПАНИИ

🏢 "Производственная группа Кайман"

📱 Телефон: {self.company_contacts['phone']}
📍 Адрес: {self.company_contacts['address']}
📧 Email: {self.company_contacts['email']}

⏰ Время работы: Пн-Пт 9:00-18:00

🚚 Доставка по всей России
        """
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🛒 Сделать заказ", callback_data="order_contacts"),
            telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
        )
        
        bot.send_message(chat_id, text, reply_markup=markup)

    def start_order_process(self, chat_id, product_key=None):
        """
        Начинает процесс заказа
        """
        self.user_states[chat_id] = {
            "state": "waiting_name",
            "product": product_key,
            "order_data": {}
        }
        
        text = """
🛒 ОФОРМЛЕНИЕ ЗАКАЗА

Для оформления заказа мне нужны ваши контактные данные.

Пожалуйста, введите ваше имя:
        """
        
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("🔙 Отмена"))
        
        bot.send_message(chat_id, text, reply_markup=markup)

    def process_order_data(self, chat_id, message_text):
        """
        Обрабатывает данные заказа
        """
        if chat_id not in self.user_states:
            return
        
        state = self.user_states[chat_id]
        
        if state["state"] == "waiting_name":
            state["order_data"]["name"] = message_text
            state["state"] = "waiting_phone"
            
            bot.send_message(chat_id, "📱 Теперь введите ваш номер телефона:")
            
        elif state["state"] == "waiting_phone":
            state["order_data"]["phone"] = message_text
            state["state"] = "waiting_address"
            
            bot.send_message(chat_id, "📍 Введите адрес доставки:")
            
        elif state["state"] == "waiting_address":
            state["order_data"]["address"] = message_text
            state["state"] = "waiting_quantity"
            
            product_name = "товар"
            if state["product"]:
                product_name = self.products_db[state["product"]]["name"]
            
            bot.send_message(chat_id, f"📦 Укажите количество {product_name}:")

    def complete_order(self, chat_id, quantity):
        """
        Завершает заказ
        """
        if chat_id not in self.user_states:
            return
        
        state = self.user_states[chat_id]
        order_data = state["order_data"]
        order_data["quantity"] = quantity
        order_data["product"] = state["product"]
        order_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Сохраняем заказ
        order_id = f"order_{int(time.time())}"
        self.orders[order_id] = order_data
        
        # Формируем сообщение о заказе
        product_name = "товар"
        if state["product"]:
            product_name = self.products_db[state["product"]]["name"]
        
        order_text = f"""
✅ ЗАКАЗ ОФОРМЛЕН!

📋 Номер заказа: {order_id}
👤 Имя: {order_data['name']}
📱 Телефон: {order_data['phone']}
📍 Адрес: {order_data['address']}
📦 Товар: {product_name}
🔢 Количество: {quantity}
📅 Дата: {order_data['date']}

📞 Менеджер свяжется с вами в течение 15 минут для подтверждения заказа и уточнения деталей.

Спасибо за заказ! 😊
        """
        
        # Отправляем заявку на email (в реальном проекте здесь была бы отправка)
        self.send_order_to_email(order_data, order_id)
        
        # Очищаем состояние пользователя
        del self.user_states[chat_id]
        
        bot.send_message(chat_id, order_text, reply_markup=self.get_main_menu())

    def send_order_to_email(self, order_data, order_id):
        """
        Отправляет заявку на email (заглушка)
        """
        # В реальном проекте здесь была бы отправка email
        print(f"ЗАЯВКА ОТПРАВЛЕНА НА {self.company_contacts['order_email']}")
        print(f"ID заказа: {order_id}")
        print(f"Данные: {json.dumps(order_data, ensure_ascii=False, indent=2)}")

    def show_help(self, chat_id):
        """
        Показывает справку
        """
        help_text = """
❓ ПОМОЩЬ

🤖 Я Добрыня, консультант по колючим заграждениям и сетке рабице.

🔧 Что я умею:
• Помогать с выбором товаров
• Рассчитывать стоимость
• Принимать заявки
• Отвечать на вопросы

📦 Наша продукция:
• Сетка рабица оцинкованная
• Колючая проволока ГОСТ 285-69
• Спиральный барьер безопасности СББ АКЛ
• Плоский барьер безопасности ПББ АКЛ
• Плоское колючее ленточное заграждение ПКЛЗ "Акация"

📞 Для заказа используйте кнопку "Сделать заказ" или позвоните: +7 (910) 598-29-58
        """
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("📞 Контакты", callback_data="show_contacts"),
            telebot.types.InlineKeyboardButton("🛒 Сделать заказ", callback_data="order_contacts"),
            telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
        )
        
        bot.send_message(chat_id, help_text, reply_markup=markup)

# Создаем экземпляр ассистента
assistant = TelegramSalesAssistant()

# Обработчики команд
@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    assistant.show_welcome_message(message.chat.id)

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды /help"""
    assistant.show_help(message.chat.id)

@bot.message_handler(commands=['catalog'])
def catalog_command(message):
    """Обработчик команды /catalog"""
    assistant.show_catalog(message.chat.id)

@bot.message_handler(commands=['contacts'])
def contacts_command(message):
    """Обработчик команды /contacts"""
    assistant.show_contacts(message.chat.id)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Обработчик текстовых сообщений"""
    chat_id = message.chat.id
    text = message.text
    
    # Проверяем состояние пользователя
    if chat_id in assistant.user_states:
        if text == "🔙 Отмена":
            del assistant.user_states[chat_id]
            bot.send_message(chat_id, "❌ Заказ отменен", reply_markup=assistant.get_main_menu())
            return
        
        # Обрабатываем данные заказа
        if assistant.user_states[chat_id]["state"] == "waiting_quantity":
            try:
                quantity = int(text)
                assistant.complete_order(chat_id, quantity)
            except ValueError:
                bot.send_message(chat_id, "❌ Пожалуйста, введите число:")
        else:
            assistant.process_order_data(chat_id, text)
        return
    
    # Обработка обычных сообщений
    if text == "📦 Каталог товаров":
        assistant.show_catalog(chat_id)
    elif text == "💰 Акции и цены":
        assistant.show_promotions(chat_id)
    elif text == "📞 Контакты":
        assistant.show_contacts(chat_id)
    elif text == "🛒 Сделать заказ":
        assistant.start_order_process(chat_id)
    elif text == "❓ Помощь":
        assistant.show_help(chat_id)
    else:
        # Обработка вопросов пользователя
        response = assistant.get_response_to_question(text)
        bot.send_message(chat_id, response)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Обработчик callback-запросов"""
    chat_id = call.message.chat.id
    data = call.data
    
    if data.startswith("product_"):
        product_key = data.replace("product_", "")
        assistant.show_product_info(chat_id, product_key)
    
    elif data.startswith("order_"):
        if data == "order_contacts":
            assistant.start_order_process(chat_id)
        elif data == "order_calculate":
            bot.send_message(chat_id, "📊 Для расчета стоимости оставьте контакты - менеджер перезвонит!")
        elif data == "order_delivery":
            bot.send_message(chat_id, "🚚 Доставка по всей России! Оставьте контакты для расчета стоимости доставки.")
        else:
            product_key = data.replace("order_", "")
            assistant.start_order_process(chat_id, product_key)
    
    elif data == "show_contacts":
        assistant.show_contacts(chat_id)
    
    elif data == "back_to_catalog":
        assistant.show_catalog(chat_id)
    
    elif data == "back_to_main":
        bot.send_message(chat_id, "🔙 Возвращаемся в главное меню", reply_markup=assistant.get_main_menu())
    
    # Отвечаем на callback
    bot.answer_callback_query(call.id)

def get_response_to_question(self, question):
    """
    Получение ответа на вопрос пользователя
    """
    question_lower = question.lower()
    
    # Приветствие
    if any(word in question_lower for word in ['привет', 'здравствуй', 'добрый день', 'добрый вечер']):
        return "Привет! 👋 Я Добрыня, консультант по колючим заграждениям. Чем могу помочь?"
    
    # Цены
    if any(word in question_lower for word in ['цена', 'стоимость', 'сколько стоит']):
        return "Цены зависят от товара и объема. Посмотрите каталог или оставьте контакты - менеджер перезвонит с точными ценами!"
    
    # Доставка
    if any(word in question_lower for word in ['доставка', 'доставить', 'курьер']):
        return "Доставка по всей России! Стоимость зависит от адреса и объема. Оставьте контакты для расчета!"
    
    # Общий ответ
    return "Интересный вопрос! 🤔 Для получения подробной информации выберите нужный раздел в меню или оставьте контакты - менеджер перезвонит!"

# Добавляем метод в класс
TelegramSalesAssistant.get_response_to_question = get_response_to_question

def main():
    """
    Основная функция запуска бота
    """
    print("🤖 Запуск Telegram бота-ассистента...")
    print(f"📱 Бот: @{(bot.get_me()).username}")
    print("✅ Бот запущен и готов к работе!")
    
    # Запускаем бота
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()