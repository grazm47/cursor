import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
import base64
import time
from datetime import datetime
import urllib3

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Инициализация бота
BOT_TOKEN = "8303280861:AAH6Z7yrqnzD-S1NfhZUOcFwizK4gPjfksc"
bot = telebot.TeleBot(BOT_TOKEN)

class DobrynyaAIDebugBot:
    def __init__(self):
        # GigaChat API настройки
        self.api_key = "ZDZjNGMzZjktMDhmYi00ZWE3LTk5MDMtYWE0OGZiZjZjMGU1OmMyOTk0MmE0LWM5NjgtNDEzZi05NjEzLTg0MWIxNTI2ZDAxMQ=="
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires = 0
        self.ai_available = False
        
        # База данных продуктов
        self.products_db = {
            "сетка_рабица": {
                "name": "Сетка рабица оцинкованная",
                "description": "Универсальный материал для ограждений, клеток, армирования",
                "specs": {
                    "высота_рулона": "0,5-3 метра",
                    "размер_ячейки": "20, 25, 30, 35, 40, 45, 50, 55, 60, 80 мм",
                    "толщина_проволоки": "1,4-3 мм",
                    "покрытие": "Оцинкованное"
                },
                "applications": [
                    "Монтаж заборов и ограждений",
                    "Армирование штукатурки",
                    "Создание клеток и вольеров",
                    "Защита вентиляционных систем",
                    "Обустройство парников и теплиц"
                ],
                "prices": {
                    "1,6мм_20x20_1,5x10м": 3540,
                    "1,6мм_30x30_1,5x10м": 2100,
                    "1,6мм_45x45_1,5x10м": 1100,
                    "1,8мм_25x25_1,5x10м": 3609,
                    "2,0мм_50x50_1,5x10м": 1675,
                    "2,5мм_50x50_1,5x10м": 2600
                }
            },
            "сбб_акл": {
                "name": "Спиральный барьер безопасности СББ АКЛ",
                "description": "Объёмная защитная конструкция из спирали колючей оцинкованной ленты",
                "specs": {
                    "диаметр_спирали": "300-1500 мм",
                    "количество_витков": "15-105",
                    "количество_клёпок": "3, 5, 7, 11",
                    "материал_сердечника": "Проволока стальная 2-2,5 мм",
                    "толщина_ленты": "0,35-0,5 мм",
                    "рабочая_длина": "4-20 метров"
                },
                "applications": [
                    "Частные территории: дома, дачи, коттеджи",
                    "Промышленные объекты: склады, заводы",
                    "Военные объекты: охрана режимных зон",
                    "Сельское хозяйство: защита урожаев",
                    "Общественные зоны: предотвращение вандализма"
                ]
            },
            "пбб_акл": {
                "name": "Плоский барьер безопасности ПББ АКЛ",
                "description": "Плоские витки, скрепленные скобами для максимальной эффективности",
                "specs": {
                    "конструкция": "Плоские витки, скрепленные скобами",
                    "материалы": "Армированная колючая лента с цинковым покрытием",
                    "срок_службы": "До 25 лет",
                    "монтаж": "На Г и I-образные кронштейны"
                },
                "applications": [
                    "Охрана входных групп: калитки, ворота",
                    "Ограда периметра: промышленные объекты, частные владения",
                    "Наземные защитные конструкции",
                    "Городские условия: общественные пространства"
                ]
            },
            "пклз_акация": {
                "name": "Плоское колючее ленточное заграждение ПКЛЗ 'Акация'",
                "description": "Сетчатое полотно из армированной колючей ленты",
                "specs": {
                    "толщина_ленты": "От 0,35 мм (ГОСТ 14918-84)",
                    "диаметр_проволоки": "От 2 мм (ГОСТ 7372-79)",
                    "расстояние_между_шипами": "30 мм",
                    "ширина_шипов": "15 мм",
                    "ячейки": "Ромбовидные, размер по требованию"
                },
                "applications": [
                    "Военные объекты и стратегические сооружения",
                    "Аэропорты и транспортные узлы",
                    "Промышленные предприятия",
                    "Частные территории и дачные участки",
                    "Природоохранные зоны",
                    "Исправительные учреждения"
                ]
            },
            "колючая_проволока": {
                "name": "Колючая проволока ГОСТ 285-69",
                "description": "Надёжное решение для создания защитных ограждений",
                "specs": {
                    "диаметр_проволоки_основы": "2,8 мм",
                    "диаметр_проволоки_шипа": "2 мм",
                    "покрытие": "Цинковое",
                    "метраж_в_бухте": "50, 100, 200, 400 м",
                    "вес_бухты_400м": "35 кг",
                    "габариты_бухты_400м": "600х600х300 мм"
                },
                "price": "5460 рублей за бухту 400 метров (35 кг)",
                "applications": [
                    "Защитные ограждения любого типа",
                    "Периметральная защита",
                    "Временные заграждения",
                    "Усиление существующих ограждений"
                ]
            }
        }
        
        # Акции и спецпредложения
        self.promotions = {
            "весенняя_акция": {
                "title": "🌱 Весенняя акция на сетку рабицу!",
                "description": "Скидка 15% на всю сетку рабицу при заказе от 5 рулонов",
                "valid_until": "30 апреля 2024"
            },
            "монтаж_бесплатно": {
                "title": "🔧 Бесплатный монтаж!",
                "description": "При заказе СББ АКЛ или ПББ АКЛ на сумму от 50 000 рублей - монтаж в подарок!",
                "valid_until": "31 мая 2024"
            },
            "оптовая_скидка": {
                "title": "📦 Оптовые цены",
                "description": "При заказе от 100 000 рублей - дополнительная скидка 10%",
                "valid_until": "Постоянно"
            }
        }
        
        # Контакты компании
        self.company_contacts = {
            "телефон": "+7 (910) 598-29-58",
            "адрес": "г. Людиново, ул. Пролетарская 145",
            "email": "kaiman40@mail.ru",
            "сайт": "https://kaiman40.ru/"
        }
        
        # Состояния пользователей
        self.user_states = {}
        self.orders = {}
        self.conversation_history = {}
        
        # Тестируем подключение к AI при запуске
        self.test_ai_connection()

    def test_ai_connection(self):
        """Тестирует подключение к GigaChat API"""
        try:
            print("🧠 Тестирование подключения к GigaChat API...")
            access_token = self._get_access_token()
            if access_token:
                print("✅ GigaChat API доступен!")
                self.ai_available = True
            else:
                print("❌ GigaChat API недоступен, используем локальную базу знаний")
                self.ai_available = False
        except Exception as e:
            print(f"❌ Ошибка тестирования AI: {e}")
            self.ai_available = False

    def _get_access_token(self):
        """Получение токена доступа к GigaChat API"""
        try:
            if self.access_token and time.time() < self.token_expires:
                return self.access_token
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'RqUID': '1234567890'
            }
            
            data = {
                'scope': 'GIGACHAT_API_PERS'
            }
            
            response = requests.post(
                f"{self.base_url}/auth",
                headers=headers,
                data=data,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                self.token_expires = time.time() + token_data.get('expires_in', 300) - 30
                return self.access_token
            else:
                print(f"❌ Ошибка получения токена: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при получении токена: {e}")
            return None

    def get_ai_response(self, user_id, message):
        """Получение ответа от GigaChat AI"""
        if not self.ai_available:
            print("🤖 AI недоступен, используем локальную базу знаний")
            return self.get_smart_response(message)
        
        try:
            access_token = self._get_access_token()
            if not access_token:
                print("❌ Не удалось получить токен, используем локальную базу знаний")
                return self.get_smart_response(message)
            
            # Системный промпт для Добрыни
            system_prompt = """Ты Добрыня, консультант в чате компании "Производственная группа Кайман", которая занимается производством, продажей и профессиональным монтажом колючих заграждений, а также производством сетки рабицы из оцинкованной проволоки.

КОММУНИКАЦИЯ ВСЕГДА ОТ ПЕРВОГО ЛИЦА МУЖСКОГО РОДА.

Ты консультируешь посетителей по колючим заграждениям и сетке рабице. Ответы должны быть лаконичными, дружелюбными, максимум 500 символов. Поддерживай уверенный, профессиональный и аутентичный стиль общения.

ЕСЛИ КЛИЕНТ ХОЧЕТ СДЕЛАТЬ ЗАКАЗ, УЗНАТЬ ЦЕНУ, ПРОСИТ СВЯЗАТЬ С МЕНЕДЖЕРОМ - ПРЕДЛОЖИ ОСТАВИТЬ EMAIL, ТЕЛЕФОН И ИМЯ ДЛЯ СВЯЗИ.

Если пользователь задает вопросы не относящиеся к тематике, отвечай с юмором. Старайся задавать наводящие вопросы, используй методологию СПИН продаж.

БАЗА ЗНАНИЙ О ПРОДУКЦИИ:
- СББ АКЛ (спиральный барьер безопасности): диаметр 300-1500мм, 15-105 витков, цена по запросу
- ПББ АКЛ (плоский барьер безопасности): срок службы до 25 лет, монтаж на кронштейны
- ПКЛЗ "Акация": сетчатое полотно, ромбовидные ячейки, для особых объектов
- Колючая проволока ГОСТ 285-69: 5460 рублей за бухту 400м (35кг)
- Сетка рабица: ячейки 20-80мм, высота 0,5-3м, цены от 1100 рублей

КОНТАКТЫ: +7 (910) 598-29-58, kaiman40@mail.ru, г. Людиново"""

            # Получаем историю разговора для пользователя
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Добавляем новое сообщение в историю
            self.conversation_history[user_id].append({"role": "user", "content": message})
            
            # Ограничиваем историю последними 10 сообщениями
            if len(self.conversation_history[user_id]) > 10:
                self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
            
            # Формируем запрос к API
            payload = {
                "model": "GigaChat:latest",
                "messages": [
                    {"role": "system", "content": system_prompt}
                ] + self.conversation_history[user_id],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=False,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Добавляем ответ AI в историю
                self.conversation_history[user_id].append({"role": "assistant", "content": ai_response})
                
                print("✅ Ответ получен от GigaChat AI")
                return ai_response
            else:
                print(f"❌ Ошибка API GigaChat: {response.status_code} - {response.text}")
                return self.get_smart_response(message)
                
        except Exception as e:
            print(f"❌ Ошибка при получении ответа от AI: {e}")
            return self.get_smart_response(message)

    def get_smart_response(self, message):
        """Умный ответ на основе локальной базы знаний"""
        message_lower = message.lower()
        
        # Проверяем на ключевые слова о продуктах
        if any(word in message_lower for word in ['колючка', 'колючая', 'проволока']):
            if 'цена' in message_lower or 'стоимость' in message_lower:
                return "💰 Колючая проволока ГОСТ 285-69 стоит 5460 рублей за бухту 400 метров (35 кг). Есть и другие варианты! Хотите узнать подробности? 📞"
            return "⚡ У нас есть колючая проволока ГОСТ 285-69 - надёжная защита для любого ограждения! Диаметр 2,8мм, оцинкованная. Нужна консультация? 😊"
        
        elif any(word in message_lower for word in ['сетка', 'рабица']):
            if 'дешевая' in message_lower or 'недорого' in message_lower:
                return "💸 Самая доступная сетка рабица - 1,6мм 45x45мм 1,5x10м за 1100 рублей! Отличный выбор для дачи. Закажете? 📞"
            return "🔗 Сетка рабица оцинкованная - универсальный материал! Ячейки от 20 до 80мм, высота до 3м. Какой размер нужен? 🤔"
        
        elif any(word in message_lower for word in ['спираль', 'сбб', 'барьер']):
            return "🌀 СББ АКЛ - спиральный барьер безопасности! Диаметр 300-1500мм, 15-105 витков. Максимальная защита! Нужен расчёт? 💪"
        
        elif any(word in message_lower for word in ['плоский', 'пбб']):
            return "📏 ПББ АКЛ - плоский барьер! Компактный, эффективный, срок службы до 25 лет. Идеален для городских условий! Интересует? 🏙️"
        
        elif any(word in message_lower for word in ['акация', 'пклз']):
            return "🌿 ПКЛЗ 'Акация' - сетчатое полотно из колючей ленты! Малозаметное, прочное, ромбовидные ячейки. Востребовано для особых объектов! 🔒"
        
        elif any(word in message_lower for word in ['доставка', 'доставить']):
            return "🚚 Доставка по всей России! Транспортными компаниями или собственным транспортом. Рассчитаю стоимость доставки - укажите адрес! 📍"
        
        elif any(word in message_lower for word in ['монтаж', 'установка']):
            return "🔧 Профессиональный монтаж силами наших специалистов! Гарантия качества. При заказе от 50 000₽ - монтаж бесплатно! Хотите? 🛠️"
        
        elif any(word in message_lower for word in ['оплата', 'платить', 'деньги']):
            return "💳 Оплата: наличные, безналичный расчёт, карта. Возможна рассрочка! Обсудим условия при заказе. Удобно? 😊"
        
        elif any(word in message_lower for word in ['гарантия', 'возврат']):
            return "✅ Гарантия качества на всю продукцию! Используем только сертифицированные материалы. Строгий контроль на всех этапах! 🏆"
        
        elif any(word in message_lower for word in ['менеджер', 'консультант']):
            return "👨‍💼 Я Добрыня, ваш персональный консультант! Но могу связать с менеджером. Оставьте контакты - перезвоним! 📞"
        
        elif any(word in message_lower for word in ['анекдот', 'шутка', 'юмор']):
            return "😄 Ха! Сетка рабица такая надёжная, что даже воры говорят: 'Лучше через колючку, чем через рабицу!' 😂 А если серьёзно - качество наше проверено временем! 💪"
        
        elif any(word in message_lower for word in ['как дела', 'как ты', 'здоровье']):
            return "😊 Отлично! Готов помогать с выбором заграждений! У нас отличная продукция - СББ АКЛ, ПББ АКЛ, сетка рабица. Что интересует? 🤔"
        
        elif any(word in message_lower for word in ['кто ты', 'имя', 'зовут']):
            return "👋 Меня зовут Добрыня! Консультант 'Производственной группы Кайман'. Помогаю с колючими заграждениями и сеткой рабицей! 😊"
        
        elif any(word in message_lower for word in ['привет', 'здравствуй', 'добрый день']):
            return "👋 Привет! Я Добрыня, консультант 'Производственной группы Кайман'! Готов помочь с выбором колючих заграждений и сетки рабицы. Что интересует? 😊"
        
        elif any(word in message_lower for word in ['пока', 'до свидания', 'прощай']):
            return "👋 До свидания! Буду рад помочь снова! Если понадобится консультация по заграждениям - обращайтесь! 📞"
        
        else:
            return "🤔 Интересный вопрос! Но я специализируюсь на колючих заграждениях и сетке рабице. Могу рассказать о СББ АКЛ, ПББ АКЛ, ПКЛЗ 'Акация' или помочь с заказом! 📞"

    def create_main_menu(self):
        """Создает главное меню"""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            KeyboardButton("📋 Каталог продукции"),
            KeyboardButton("💰 Акции и цены"),
            KeyboardButton("📞 Контакты"),
            KeyboardButton("🛒 Оформить заказ"),
            KeyboardButton("🤖 Задать вопрос Добрыне"),
            KeyboardButton("ℹ️ О компании")
        )
        return markup

    def create_catalog_menu(self):
        """Создает меню каталога"""
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🔗 Сетка рабица оцинкованная", callback_data="product_сетка_рабица"),
            InlineKeyboardButton("🌀 СББ АКЛ (спиральный барьер)", callback_data="product_сбб_акл"),
            InlineKeyboardButton("📏 ПББ АКЛ (плоский барьер)", callback_data="product_пбб_акл"),
            InlineKeyboardButton("🌿 ПКЛЗ 'Акация'", callback_data="product_пклз_акация"),
            InlineKeyboardButton("⚡ Колючая проволока ГОСТ 285-69", callback_data="product_колючая_проволока"),
            InlineKeyboardButton("🔙 Назад в главное меню", callback_data="main_menu")
        )
        return markup

    def get_product_info(self, product_key):
        """Возвращает информацию о продукте"""
        if product_key not in self.products_db:
            return "❌ Продукт не найден"
        
        product = self.products_db[product_key]
        info = f"🏭 {product['name']}\n\n"
        info += f"📝 {product['description']}\n\n"
        
        if 'specs' in product:
            info += "📊 Характеристики:\n"
            for key, value in product['specs'].items():
                info += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        if 'price' in product:
            info += f"\n💰 Цена: {product['price']}\n"
        elif 'prices' in product:
            info += "\n💰 Цены:\n"
            for key, price in list(product['prices'].items())[:5]:  # Показываем первые 5 цен
                info += f"• {key.replace('_', ' ')}: {price} ₽\n"
        
        if 'applications' in product:
            info += "\n🎯 Применение:\n"
            for app in product['applications'][:5]:  # Показываем первые 5 применений
                info += f"• {app}\n"
        
        info += "\n📞 Для заказа звоните: +7 (910) 598-29-58"
        return info

    def save_order(self, user_id, order_data):
        """Сохраняет заявку в файл"""
        try:
            with open('заявки.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"НОВАЯ ЗАЯВКА - {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"ID пользователя: {user_id}\n")
                for key, value in order_data.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"{'='*50}\n")
            return True
        except Exception as e:
            print(f"Ошибка сохранения заявки: {e}")
            return False

# Создание экземпляра бота
dobrynya_bot = DobrynyaAIDebugBot()

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    ai_status = "🤖 Подключен к GigaChat AI!" if dobrynya_bot.ai_available else "📚 Использует локальную базу знаний"
    
    welcome_text = f"""👋 Привет! Я Добрыня, консультант "Производственной группы Кайман"! 

🏭 Мы производим и продаём:
• Спиральные барьеры безопасности СББ АКЛ
• Плоские барьеры безопасности ПББ АКЛ  
• Колючую проволоку ГОСТ 285-69
• Сетку рабицу оцинкованную
• ПКЛЗ "Акация"

💪 Профессиональный монтаж и доставка по всей России!
{ai_status}

Выберите, что вас интересует:"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=dobrynya_bot.create_main_menu())

@bot.message_handler(func=lambda message: message.text == "📋 Каталог продукции")
def show_catalog(message):
    """Показывает каталог продукции"""
    catalog_text = "🏭 Наша продукция:\n\nВыберите интересующий товар:"
    bot.send_message(message.chat.id, catalog_text, reply_markup=dobrynya_bot.create_catalog_menu())

@bot.message_handler(func=lambda message: message.text == "💰 Акции и цены")
def show_promotions(message):
    """Показывает акции и спецпредложения"""
    promo_text = "🎉 Актуальные акции и спецпредложения:\n\n"
    
    for key, promo in dobrynya_bot.promotions.items():
        promo_text += f"{promo['title']}\n"
        promo_text += f"📝 {promo['description']}\n"
        promo_text += f"⏰ Действует до: {promo['valid_until']}\n\n"
    
    promo_text += "📞 Для получения персонального предложения звоните: +7 (910) 598-29-58"
    bot.send_message(message.chat.id, promo_text)

@bot.message_handler(func=lambda message: message.text == "📞 Контакты")
def show_contacts(message):
    """Показывает контакты компании"""
    contacts_text = """📞 Контакты "Производственной группы Кайман":

📱 Телефон: +7 (910) 598-29-58
📍 Адрес: г. Людиново, ул. Пролетарская 145
📧 Email: kaiman40@mail.ru
🌐 Сайт: https://kaiman40.ru/

⏰ Режим работы: Пн-Пт 9:00-18:00

🚚 Доставка по всей России!
🔧 Профессиональный монтаж!"""
    
    bot.send_message(message.chat.id, contacts_text)

@bot.message_handler(func=lambda message: message.text == "🛒 Оформить заказ")
def start_order(message):
    """Начинает процесс оформления заказа"""
    order_text = """🛒 Оформление заказа

Для оформления заказа мне нужна следующая информация:

1️⃣ Ваше имя
2️⃣ Номер телефона
3️⃣ Email (если есть)
4️⃣ Что хотите заказать
5️⃣ Адрес доставки
6️⃣ Желаемая дата доставки

Начнём? Отправьте ваше имя:"""
    
    dobrynya_bot.user_states[message.chat.id] = "waiting_name"
    bot.send_message(message.chat.id, order_text)

@bot.message_handler(func=lambda message: message.text == "🤖 Задать вопрос Добрыне")
def ask_ai_question(message):
    """Обработчик для вопросов к AI"""
    ai_status = "GigaChat AI" if dobrynya_bot.ai_available else "локальной базе знаний"
    
    question_text = f"""🤖 Задайте любой вопрос Добрыне!

Я использую {ai_status} и могу ответить на любые вопросы о:
• Характеристиках товаров
• Ценах и акциях
• Доставке и монтаже
• Гарантии и качестве
• И многом другом!

Просто напишите ваш вопрос:"""
    
    dobrynya_bot.user_states[message.chat.id] = "waiting_ai_question"
    bot.send_message(message.chat.id, question_text)

@bot.message_handler(func=lambda message: message.text == "ℹ️ О компании")
def about_company(message):
    """Информация о компании"""
    ai_status = "AI-консультант Добрыня (GigaChat)" if dobrynya_bot.ai_available else "AI-консультант Добрыня (локальная база знаний)"
    
    about_text = f"""🏭 "Производственная группа Кайман"

Мы специализируемся на производстве, продаже и профессиональном монтаже колючих заграждений, а также производстве сетки рабицы из оцинкованной проволоки.

🎯 Наша продукция:
• СББ АКЛ - спиральные барьеры безопасности
• ПББ АКЛ - плоские барьеры безопасности
• Колючая проволока ГОСТ 285-69
• Сетка рабица оцинкованная
• ПКЛЗ "Акация"

✅ Преимущества:
• Собственное производство
• Конкурентоспособные цены
• Профессиональный монтаж
• Доставка по всей России
• Гарантия качества
• {ai_status}

📞 Свяжитесь с нами для консультации!"""
    
    bot.send_message(message.chat.id, about_text)

@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def handle_product_callback(call):
    """Обработчик выбора продукта"""
    product_key = call.data.replace('product_', '')
    product_info = dobrynya_bot.get_product_info(product_key)
    
    # Создаем кнопки для действий с продуктом
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛒 Заказать", callback_data=f"order_{product_key}"),
        InlineKeyboardButton("💰 Узнать цену", callback_data=f"price_{product_key}"),
        InlineKeyboardButton("📞 Консультация", callback_data="consultation"),
        InlineKeyboardButton("🔙 Назад в каталог", callback_data="catalog")
    )
    
    bot.edit_message_text(
        product_info,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def back_to_main_menu(call):
    """Возврат в главное меню"""
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "catalog")
def back_to_catalog(call):
    """Возврат в каталог"""
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_catalog(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def handle_order_callback(call):
    """Обработчик заказа продукта"""
    product_key = call.data.replace('order_', '')
    product_name = dobrynya_bot.products_db[product_key]['name']
    
    order_text = f"""🛒 Заказ: {product_name}

Для оформления заказа оставьте контакты:

📞 Телефон: +7 (910) 598-29-58
📧 Email: kaiman40@mail.ru

Или заполните форму заказа прямо здесь!"""
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 Заполнить форму", callback_data="fill_order_form"))
    
    bot.edit_message_text(
        order_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: dobrynya_bot.user_states.get(message.chat.id) == "waiting_name")
def handle_name(message):
    """Обработчик имени в заказе"""
    user_id = message.chat.id
    dobrynya_bot.orders[user_id] = {"имя": message.text}
    dobrynya_bot.user_states[user_id] = "waiting_phone"
    
    bot.send_message(user_id, f"👋 Отлично, {message.text}! Теперь отправьте ваш номер телефона:")

@bot.message_handler(func=lambda message: dobrynya_bot.user_states.get(message.chat.id) == "waiting_phone")
def handle_phone(message):
    """Обработчик телефона в заказе"""
    user_id = message.chat.id
    dobrynya_bot.orders[user_id]["телефон"] = message.text
    dobrynya_bot.user_states[user_id] = "waiting_product"
    
    bot.send_message(user_id, "📱 Телефон записан! Теперь укажите, что хотите заказать:")

@bot.message_handler(func=lambda message: dobrynya_bot.user_states.get(message.chat.id) == "waiting_product")
def handle_product(message):
    """Обработчик продукта в заказе"""
    user_id = message.chat.id
    dobrynya_bot.orders[user_id]["продукт"] = message.text
    dobrynya_bot.user_states[user_id] = "waiting_address"
    
    bot.send_message(user_id, "📦 Продукт записан! Укажите адрес доставки:")

@bot.message_handler(func=lambda message: dobrynya_bot.user_states.get(message.chat.id) == "waiting_address")
def handle_address(message):
    """Обработчик адреса в заказе"""
    user_id = message.chat.id
    order_data = dobrynya_bot.orders[user_id]
    order_data["адрес"] = message.text
    
    # Сохраняем заявку
    if dobrynya_bot.save_order(user_id, order_data):
        success_text = f"""✅ Заявка успешно оформлена!

📋 Ваши данные:
👤 Имя: {order_data['имя']}
📱 Телефон: {order_data['телефон']}
📦 Продукт: {order_data['продукт']}
📍 Адрес: {order_data['адрес']}

📞 Наш менеджер свяжется с вами в ближайшее время!
📧 Заявка отправлена на: grazm47@yandex.ru

Спасибо за заказ! 😊"""
    else:
        success_text = "❌ Ошибка при сохранении заявки. Попробуйте позже или позвоните: +7 (910) 598-29-58"
    
    # Очищаем состояние пользователя
    del dobrynya_bot.user_states[user_id]
    del dobrynya_bot.orders[user_id]
    
    bot.send_message(user_id, success_text, reply_markup=dobrynya_bot.create_main_menu())

@bot.message_handler(func=lambda message: dobrynya_bot.user_states.get(message.chat.id) == "waiting_ai_question")
def handle_ai_question(message):
    """Обработчик вопросов к AI"""
    user_id = message.chat.id
    question = message.text
    
    # Отправляем сообщение о том, что AI думает
    thinking_msg = bot.send_message(user_id, "🤔 Добрыня думает...")
    
    # Получаем ответ от AI или локальной базы знаний
    ai_response = dobrynya_bot.get_ai_response(user_id, question)
    
    # Удаляем сообщение "думает"
    bot.delete_message(user_id, thinking_msg.message_id)
    
    # Очищаем состояние
    del dobrynya_bot.user_states[user_id]
    
    bot.send_message(user_id, ai_response, reply_markup=dobrynya_bot.create_main_menu())

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработчик всех остальных сообщений"""
    # Если пользователь в процессе заказа, игнорируем
    if message.chat.id in dobrynya_bot.user_states:
        return
    
    # Пытаемся ответить через AI или локальную базу знаний
    ai_response = dobrynya_bot.get_ai_response(message.chat.id, message.text)
    bot.send_message(message.chat.id, ai_response, reply_markup=dobrynya_bot.create_main_menu())

def main():
    """Главная функция"""
    print("🤖 Запуск Telegram бота Добрыня с AI...")
    print("🧠 Тестирование подключения к GigaChat...")
    
    if dobrynya_bot.ai_available:
        print("✅ GigaChat AI доступен!")
    else:
        print("📚 Используется локальная база знаний")
    
    print("📱 Бот готов к работе!")
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()