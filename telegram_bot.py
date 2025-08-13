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
        Инициализация Telegram ассистента-продавца (полная база знаний Добрыни)
        """
        # База данных товаров (полная база знаний)
        self.products_db = {
            "сетка_рабица": {
                "name": "Сетка рабица оцинкованная",
                "prices": {
                    "45x45_1.6": {"price": 1100, "description": "45×45 мм (1,6 мм) - 1,5×10 м"},
                    "50x50_1.6": {"price": 1130, "description": "50×50 мм (1,6 мм) - 1,5×10 м"},
                    "60x60_2.0": {"price": 1365, "description": "60×60 мм (2,0 мм) - 1,5×10 м"}
                },
                "description": "Универсальный материал для ограждений, вольеров, армирования",
                "specs": {
                    "размер_ячеек": "20-100 мм",
                    "толщина_проволоки": "1,6-3,0 мм",
                    "ширина_рулона": "0,5-3 метра",
                    "длина_рулона": "10-25 метров",
                    "срок_службы": "Более 15 лет"
                }
            },
            "колючая_проволока": {
                "name": "Колючая проволока ГОСТ 285-69",
                "price": 5460,
                "description": "Бухта 400 метров (35 кг), диаметр основы 2,8 мм, шипа 2 мм",
                "specs": {
                    "диаметр_основы": "2,8 мм",
                    "диаметр_шипа": "2 мм",
                    "покрытие": "Цинковое",
                    "метраж_в_бухте": "50, 100, 200, 400 м",
                    "вес_400м": "35 кг",
                    "габариты_400м": "600×600×300 мм"
                }
            },
            "сбб_акл": {
                "name": "Спиральный барьер безопасности СББ АКЛ",
                "description": "Объемная защитная конструкция из спирали колючей оцинкованной ленты с металлическим сердечником",
                "specs": {
                    "диаметр_спирали": "300-1500 мм",
                    "количество_витков": "15-105",
                    "количество_клепок": "3, 5, 7, 11",
                    "рабочая_длина": "4-20 метров",
                    "материал_сердечника": "Проволока стальная",
                    "диаметр_сердечника": "2-2,5 мм",
                    "толщина_ленты": "0,35-0,5 мм"
                },
                "features": ["Высокий уровень защиты", "Усиленная конструкция", "Эффективность при любых попытках проникновения", "Универсальность применения"],
                "applications": ["Частные территории", "Промышленность", "Военные объекты", "Сельское хозяйство", "Общественные зоны"]
            },
            "пбб_акл": {
                "name": "Плоский барьер безопасности ПББ АКЛ",
                "description": "Плоские витки армированной колючей ленты, скрепленные специальными скобами",
                "specs": {
                    "конструкция": "Плоские витки, скрепленные скобами",
                    "материалы": "Армированная колючая лента с цинковым покрытием",
                    "срок_службы": "До 25 лет"
                },
                "features": ["Максимальная надежность", "Долговечность", "Экономичность", "Компактность", "Простота монтажа", "Функциональность", "Универсальность", "Незаметность"],
                "applications": ["Охрана входных групп", "Ограда периметра", "Наземные защитные конструкции", "Городские условия"]
            },
            "пклз_акация": {
                "name": "Плоское колючее ленточное заграждение ПКЛЗ 'Акация'",
                "description": "Сетчатое полотно из армированной колючей ленты (АКЛ)",
                "specs": {
                    "колючая_лента": "Оцинкованная лента толщиной от 0,35 мм (ГОСТ 14918-84)",
                    "проволока": "Высокоуглеродистая проволока диаметром от 2 мм (ГОСТ 7372-79)",
                    "шипы": "Расстояние между шипами — 30 мм, ширина шипов — 15 мм",
                    "ячейки": "Ромбовидные ячейки различных размеров"
                },
                "features": ["Малозаметность в городской среде", "Устойчивость к механическим воздействиям", "Высокий останавливающий эффект", "Отличные пружинящие свойства", "Повышенная твердость и прочность", "Устойчивость к коррозии"],
                "applications": ["Военные объекты", "Аэропорты", "Промышленные предприятия", "Частные территории", "Природоохранные зоны", "Исправительные учреждения"]
            }
        }
        
        # Акции и скидки (полная база знаний)
        self.promotions = {
            "скидка_20": "Скидка 20% на все смартфоны до конца недели!",
            "бесплатная_доставка": "Бесплатная доставка при заказе от 5000 рублей",
            "подарок": "При покупке ноутбука - бесплатные наушники в подарок!",
            "скидка_аксессуары": "Скидка 15% на аксессуары при покупке основного товара",
            "скидка_объем": "Скидки от 5% при заказе от 5 рулонов",
            "скидка_10": "Скидка 10% при заказе от 10 рулонов",
            "гарантия": "Гарантия качества на всю продукцию"
        }
        
        # Контакты компании
        self.company_contacts = {
            "phone": "+7 (910) 598-29-58",
            "address": "г. Людиново, ул. Пролетарская 145",
            "email": "kaiman40@mail.ru",
            "order_email": "grazm47@yandex.ru"
        }
        
        # Предустановленные ответы для разных типов вопросов (стиль Добрыни)
        self.responses = {
            "приветствие": [
                "Здравствуйте! Добро пожаловать в TechStore! 👋 Я готов помочь вам с выбором товаров. Что вас интересует?",
                "Приветствую! Рад видеть вас в нашем магазине! 🛍️ Чем могу помочь?",
                "Добрый день! Добро пожаловать в TechStore! 🤖 Я ваш персональный ассистент по покупкам."
            ],
            "помощь": [
                "Конечно! Я могу помочь вам с выбором товаров, рассказать об акциях, показать каталог и ответить на любые вопросы о покупках! 💡",
                "Я готов помочь! Могу показать товары, рассказать о ценах, акциях, доставке и многом другом. Что именно вас интересует? 🤔"
            ],
            "доставка": [
                "Доставка осуществляется по всей России! 🚚 Курьерская доставка - 1-2 дня, почта России - 3-7 дней. Бесплатная доставка при заказе от 5000 рублей!",
                "Мы доставляем товары курьером и почтой России. Сроки: курьер 1-2 дня, почта 3-7 дней. При заказе от 5000₽ доставка бесплатная! 📦"
            ],
            "оплата": [
                "Принимаем оплату картой онлайн, при получении наличными или картой, а также в рассрочку! 💳",
                "Способы оплаты: карта онлайн, наличные при получении, карта при получении, рассрочка до 12 месяцев! 💰"
            ],
            "возврат": [
                "Возврат товара возможен в течение 14 дней с момента получения при сохранении товарного вида! 🔄",
                "У вас есть 14 дней на возврат товара с момента получения. Главное - сохранить товарный вид! ✅"
            ],
            "заказ": [
                "Для оформления заказа выберите товар, добавьте в корзину и следуйте инструкциям на сайте! 🛒",
                "Заказ оформляется на сайте: выбираете товар, добавляете в корзину, заполняете данные и оплачиваете! 📝"
            ],
            "общие": [
                "Отличный выбор! Этот товар пользуется большой популярностью у наших покупателей! 👍",
                "Хороший вопрос! Давайте разберем это подробнее. Что именно вас интересует? 🤔",
                "Интересный вопрос! Я с удовольствием на него отвечу. 💭"
            ]
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
        Показывает приветственное сообщение (стиль Добрыни)
        """
        welcome_text = """
🤖 Привет! Я Добрыня, консультант по колючим заграждениям и сетке рабице от "Производственной группы Кайман"!

Готов помочь с выбором товаров, расчетом стоимости и оформлением заказов! 😊

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
        Показывает информацию о товаре (полная база знаний Добрыни)
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

📋 Характеристики:
• Размер ячеек: {product['specs']['размер_ячеек']}
• Толщина проволоки: {product['specs']['толщина_проволоки']}
• Ширина рулона: {product['specs']['ширина_рулона']}
• Длина рулона: {product['specs']['длина_рулона']}
• Срок службы: {product['specs']['срок_службы']}

📞 Для заказа оставьте контакты!
            """
        elif product_key == "колючая_проволока":
            text = f"""
🦔 {product['name']}

{product['description']}

💰 Цена: {product['price']}₽ за бухту

📋 Характеристики:
• Диаметр основы: {product['specs']['диаметр_основы']}
• Диаметр шипа: {product['specs']['диаметр_шипа']}
• Покрытие: {product['specs']['покрытие']}
• Метраж в бухте: {product['specs']['метраж_в_бухте']}
• Вес (400 м): {product['specs']['вес_400м']}
• Габариты (400 м): {product['specs']['габариты_400м']}

📞 Для заказа оставьте контакты!
            """
        else:
            text = f"""
{product['name']}

{product['description']}

📋 Характеристики:
"""
            for key, value in product['specs'].items():
                text += f"• {key.replace('_', ' ').title()}: {value}\n"
            
            text += f"""
✨ Преимущества:
"""
            for feature in product['features']:
                text += f"• {feature}\n"
            
            if 'applications' in product:
                text += f"""
🏢 Применение:
"""
                for app in product['applications']:
                    text += f"• {app}\n"
            
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
        Показывает акции и цены (стиль Добрыни)
        """
        text = """
💰 АКЦИИ И СПЕЦИАЛЬНЫЕ ПРЕДЛОЖЕНИЯ

🎉 Текущие акции:
"""
        for promo_id, description in self.promotions.items():
            text += f"• {description}\n"
        
        text += f"""

💡 Скидки зависят от объема заказа:
• От 5 рулонов - скидка 5%
• От 10 рулонов - скидка 10%
• Крупные заказы - индивидуальные условия

📞 Для получения персональных предложений оставьте контакты - предложим лучшие условия! 😊
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

Отлично! Для оформления заказа мне нужны ваши контактные данные.

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

Отлично! Ваш заказ успешно оформлен! 🎉

📋 Номер заказа: {order_id}
👤 Имя: {order_data['name']}
📱 Телефон: {order_data['phone']}
📍 Адрес: {order_data['address']}
📦 Товар: {product_name}
🔢 Количество: {quantity}
📅 Дата: {order_data['date']}

📞 Менеджер свяжется с вами в течение 15 минут для подтверждения заказа и уточнения деталей.

Спасибо за заказ! Буду рад помочь снова! 😊
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
        Показывает справку (стиль Добрыни)
        """
        help_text = """
❓ ПОМОЩЬ

🤖 Я Добрыня, консультант по колючим заграждениям и сетке рабице от "Производственной группы Кайман"!

🔧 Что я умею:
• Помогать с выбором товаров
• Рассчитывать стоимость
• Принимать заявки
• Отвечать на вопросы

📦 Наша продукция:
• Сетка рабица оцинкованная (от 1100₽)
• Колючая проволока ГОСТ 285-69 (5460₽ за бухту)
• Спиральный барьер безопасности СББ АКЛ
• Плоский барьер безопасности ПББ АКЛ
• Плоское колючее ленточное заграждение ПКЛЗ "Акация"

📞 Для заказа используйте кнопку "Сделать заказ" или позвоните: +7 (910) 598-29-58

Готов помочь с любыми вопросами! 😊
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
    Получение ответа на вопрос пользователя (полная база знаний Добрыни)
    """
    question_lower = question.lower()
    
    # Приветствие
    if any(word in question_lower for word in ['привет', 'здравствуй', 'добрый день', 'добрый вечер', 'доброе утро']):
        return "Привет! 👋 Я Добрыня, консультант по колючим заграждениям и сетке рабице от 'Производственной группы Кайман'. Чем могу помочь?"
    
    # Цены
    if any(word in question_lower for word in ['цена', 'стоимость', 'сколько стоит', 'дешево', 'дорого']):
        return "Цены зависят от товара и объема! Сетка рабица от 1100₽, колючая проволока 5460₽ за бухту. Оставьте контакты - менеджер перезвонит с точными ценами! 😊"
    
    # Доставка
    if any(word in question_lower for word in ['доставка', 'доставить', 'курьер', 'почта', 'транспорт']):
        return "Доставка по всей России! 🚚 Курьерская доставка - 1-2 дня, почта России - 3-7 дней. Бесплатная доставка при заказе от 5000 рублей! Оставьте контакты для расчета! 📦"
    
    # Скидки
    if any(word in question_lower for word in ['скидка', 'акция', 'дешевле', 'выгодно']):
        return "Скидки есть! 🎉 От 5 рулонов - скидка 5%, от 10 рулонов - 10%. Бесплатная доставка от 5000₽. Оставьте контакты - предложим лучшие условия! 💰"
    
    # Качество
    if any(word in question_lower for word in ['качество', 'надежность', 'гарантия', 'прочность']):
        return "Качество гарантируем! ✅ Собственное производство, контроль на всех этапах, гарантия на всю продукцию. Мы серьезная компания с 2010 года! 🏭"
    
    # Заказ
    if any(word in question_lower for word in ['заказать', 'купить', 'приобрести', 'оформить']):
        return "Отлично! 🛒 Для заказа оставьте контакты - менеджер перезвонит в течение 15 минут и оформит заказ! 📞"
    
    # Контакты
    if any(word in question_lower for word in ['контакты', 'телефон', 'адрес', 'связаться']):
        return "Наши контакты: 📱 +7 (910) 598-29-58, 📍 г. Людиново, ул. Пролетарская 145. Или оставьте свои контакты - перезвоним! 😊"
    
    # Оплата
    if any(word in question_lower for word in ['оплата', 'платить', 'карта', 'наличные', 'рассрочка']):
        return "Принимаем оплату картой онлайн, при получении наличными или картой, а также в рассрочку! 💳 Оставьте контакты - расскажем подробнее! 💰"
    
    # Возврат
    if any(word in question_lower for word in ['возврат', 'вернуть', 'обмен', 'гарантия']):
        return "Возврат товара возможен в течение 14 дней с момента получения при сохранении товарного вида! 🔄 Оставьте контакты - уточним детали! ✅"
    
    # Сетка рабица
    if any(word in question_lower for word in ['сетка', 'рабица', 'рабица']):
        return "Сетка рабица оцинкованная - универсальный материал! 🔗 Размер ячеек 20-100 мм, толщина проволоки 1,6-3,0 мм. Цены от 1100₽ за рулон. Оставьте контакты - подберем оптимальный вариант! 😊"
    
    # Колючая проволока
    if any(word in question_lower for word in ['колючка', 'колючая', 'проволока', 'егоза']):
        return "Колючая проволока ГОСТ 285-69 - надежная защита! 🦔 Диаметр основы 2,8 мм, шипа 2 мм. Цена 5460₽ за бухту 400 м. Оставьте контакты - оформим заказ! 📞"
    
    # СББ АКЛ
    if any(word in question_lower for word in ['сбб', 'спиральный', 'барьер', 'спираль']):
        return "СББ АКЛ - спиральный барьер безопасности! 🌀 Диаметр 300-1500 мм, длина 4-20 м. Высокий уровень защиты, универсальность применения. Оставьте контакты - рассчитаем стоимость! 🛡️"
    
    # ПББ АКЛ
    if any(word in question_lower for word in ['пбб', 'плоский', 'барьер']):
        return "ПББ АКЛ - плоский барьер безопасности! 📏 Плоские витки, скрепленные скобами, срок службы до 25 лет. Компактность и простота монтажа. Оставьте контакты - подберем размер! 🏗️"
    
    # ПКЛЗ Акация
    if any(word in question_lower for word in ['акация', 'пклз', 'ленточное', 'заграждение']):
        return "ПКЛЗ 'Акация' - плоское колючее ленточное заграждение! 🌿 Сетчатое полотно из армированной колючей ленты. Малозаметность и высокий останавливающий эффект. Оставьте контакты - расскажем подробнее! 🛡️"
    
    # Общие вопросы
    if any(word in question_lower for word in ['что', 'как', 'где', 'когда', 'почему']):
        return "Интересный вопрос! 🤔 Для получения подробной информации выберите нужный раздел в меню или оставьте контакты - менеджер перезвонит! 💡"
    
    # Общий ответ (стиль Добрыни)
    return "Хороший вопрос! 😊 Я Добрыня, специализируюсь на колючих заграждениях и сетке рабице. Выберите нужный раздел в меню или оставьте контакты - помогу с выбором! 🤖"

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