#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демо-версия ассистента-продавца без API GigaChat
Работает локально с предустановленными ответами
"""

import os
import sys
import random
from typing import Optional, Dict, Any, List

class DemoSalesAssistant:
    def __init__(self):
        """
        Инициализация демо-ассистента-продавца
        """
        # База данных товаров
        self.products_db = {
            "смартфоны": [
                {"name": "iPhone 15 Pro", "price": 99990, "description": "Новейший iPhone с титановым корпусом", "stock": 15},
                {"name": "Samsung Galaxy S24", "price": 89990, "description": "Флагманский Android смартфон", "stock": 12},
                {"name": "Xiaomi 14", "price": 69990, "description": "Отличное соотношение цена-качество", "stock": 20},
                {"name": "Huawei P60 Pro", "price": 79990, "description": "Мощная камера и стильный дизайн", "stock": 8}
            ],
            "ноутбуки": [
                {"name": "MacBook Pro 14", "price": 199990, "description": "Мощный ноутбук для профессионалов", "stock": 8},
                {"name": "Dell XPS 13", "price": 149990, "description": "Ультрабук премиум класса", "stock": 10},
                {"name": "Lenovo ThinkPad X1", "price": 179990, "description": "Бизнес-ноутбук высшего класса", "stock": 6},
                {"name": "ASUS ROG Strix", "price": 129990, "description": "Игровой ноутбук с мощной графикой", "stock": 12}
            ],
            "наушники": [
                {"name": "AirPods Pro 2", "price": 24990, "description": "Беспроводные наушники с шумоподавлением", "stock": 25},
                {"name": "Sony WH-1000XM5", "price": 39990, "description": "Лучшие накладные наушники", "stock": 18},
                {"name": "Samsung Galaxy Buds2", "price": 15990, "description": "Компактные TWS наушники", "stock": 30},
                {"name": "Bose QuietComfort", "price": 34990, "description": "Премиум наушники с активным шумоподавлением", "stock": 15}
            ],
            "планшеты": [
                {"name": "iPad Pro 12.9", "price": 129990, "description": "Мощный планшет для профессионалов", "stock": 10},
                {"name": "Samsung Galaxy Tab S9", "price": 89990, "description": "Android планшет премиум класса", "stock": 14},
                {"name": "Xiaomi Pad 6", "price": 39990, "description": "Отличный планшет по доступной цене", "stock": 22}
            ],
            "аксессуары": [
                {"name": "Чехол для iPhone", "price": 2990, "description": "Защитный чехол из силикона", "stock": 50},
                {"name": "Беспроводная зарядка", "price": 4990, "description": "Быстрая беспроводная зарядка 15W", "stock": 35},
                {"name": "USB-C кабель", "price": 990, "description": "Высокоскоростной кабель для зарядки", "stock": 100}
            ]
        }
        
        # Акции и скидки
        self.promotions = {
            "скидка_20": "Скидка 20% на все смартфоны до конца недели!",
            "бесплатная_доставка": "Бесплатная доставка при заказе от 5000 рублей",
            "подарок": "При покупке ноутбука - бесплатные наушники в подарок!",
            "скидка_аксессуары": "Скидка 15% на аксессуары при покупке основного товара"
        }
        
        # Предустановленные ответы для разных типов вопросов
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

    def search_products(self, query: str) -> List[Dict]:
        """
        Поиск товаров по запросу
        
        Args:
            query (str): Поисковый запрос
            
        Returns:
            List[Dict]: Список найденных товаров
        """
        query_lower = query.lower()
        results = []
        
        for category, products in self.products_db.items():
            for product in products:
                if (query_lower in product["name"].lower() or 
                    query_lower in product["description"].lower() or
                    query_lower in category):
                    results.append({**product, "category": category})
        
        return results

    def get_product_info(self, product_name: str) -> Optional[Dict]:
        """
        Получение информации о конкретном товаре
        
        Args:
            product_name (str): Название товара
            
        Returns:
            Optional[Dict]: Информация о товаре
        """
        for category, products in self.products_db.items():
            for product in products:
                if product_name.lower() in product["name"].lower():
                    return {**product, "category": category}
        return None

    def get_response(self, user_input: str) -> str:
        """
        Получение ответа на основе пользовательского ввода
        
        Args:
            user_input (str): Ввод пользователя
            
        Returns:
            str: Ответ ассистента
        """
        input_lower = user_input.lower()
        
        # Приветствие
        if any(word in input_lower for word in ['привет', 'здравствуй', 'добрый день', 'добрый вечер', 'доброе утро']):
            return random.choice(self.responses["приветствие"])
        
        # Помощь
        if any(word in input_lower for word in ['помощь', 'помоги', 'что ты умеешь', 'функции']):
            return random.choice(self.responses["помощь"])
        
        # Доставка
        if any(word in input_lower for word in ['доставка', 'доставить', 'курьер', 'почта', 'сроки доставки']):
            return random.choice(self.responses["доставка"])
        
        # Оплата
        if any(word in input_lower for word in ['оплата', 'платить', 'карта', 'наличные', 'рассрочка']):
            return random.choice(self.responses["оплата"])
        
        # Возврат
        if any(word in input_lower for word in ['возврат', 'вернуть', 'обмен', 'гарантия']):
            return random.choice(self.responses["возврат"])
        
        # Заказ
        if any(word in input_lower for word in ['заказ', 'заказать', 'оформить', 'купить', 'покупка']):
            return random.choice(self.responses["заказ"])
        
        # Поиск товаров
        if any(word in input_lower for word in ['найти', 'искать', 'есть ли', 'имеется']):
            # Извлекаем поисковый запрос
            for word in ['найти', 'искать', 'есть ли', 'имеется']:
                if word in input_lower:
                    query = input_lower.split(word)[-1].strip()
                    results = self.search_products(query)
                    if results:
                        response = f"🔍 Найдено товаров по запросу '{query}':\n"
                        for product in results[:3]:  # Показываем первые 3
                            response += f"• {product['name']} - {product['price']:,} ₽ ({product['category']})\n"
                        return response
                    else:
                        return f"❌ К сожалению, товары по запросу '{query}' не найдены. Попробуйте другой поисковый запрос."
        
        # Общие вопросы
        return random.choice(self.responses["общие"])

    def show_help(self):
        """
        Показать справку по командам
        """
        help_text = """
📋 ДОСТУПНЫЕ КОМАНДЫ:

🔍 ПОИСК И КАТАЛОГ:
- "показать смартфоны" - показать все смартфоны
- "показать ноутбуки" - показать все ноутбуки  
- "показать наушники" - показать все наушники
- "показать планшеты" - показать все планшеты
- "показать аксессуары" - показать все аксессуары
- "найти [товар]" - поиск конкретного товара
- "информация о [товар]" - подробная информация о товаре

💰 АКЦИИ И ЦЕНЫ:
- "акции" - показать текущие акции
- "скидки" - показать скидки
- "цены" - показать цены на товары

📦 ЗАКАЗ И ДОСТАВКА:
- "как заказать" - информация о заказе
- "доставка" - информация о доставке
- "оплата" - способы оплаты
- "возврат" - условия возврата

❓ ПОМОЩЬ:
- "помощь" - показать эту справку
- "выход" - завершить работу

💡 ПРИМЕРЫ ВОПРОСОВ:
- "Какой смартфон лучше купить?"
- "Есть ли скидки на ноутбуки?"
- "Сколько стоит доставка?"
- "Можно ли вернуть товар?"
- "Найти iPhone"
- "Информация о MacBook"
        """
        print(help_text)

    def show_products(self, category: str = None):
        """
        Показать товары по категории
        
        Args:
            category (str, optional): Категория товаров
        """
        if category and category in self.products_db:
            products = self.products_db[category]
            emoji = {"смартфоны": "📱", "ноутбуки": "💻", "наушники": "🎧", "планшеты": "📱", "аксессуары": "🔌"}
            print(f"\n{emoji.get(category, '📦')} {category.upper()}:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product['name']} - {product['price']:,} ₽")
                print(f"   {product['description']}")
                print(f"   В наличии: {product['stock']} шт.")
                print()
        else:
            print("\n📦 ВСЕ ТОВАРЫ:")
            for category, products in self.products_db.items():
                emoji = {"смартфоны": "📱", "ноутбуки": "💻", "наушники": "🎧", "планшеты": "📱", "аксессуары": "🔌"}
                print(f"\n{emoji.get(category, '📦')} {category.upper()}:")
                for product in products:
                    print(f"  • {product['name']} - {product['price']:,} ₽")

    def show_promotions(self):
        """
        Показать текущие акции
        """
        print("\n🎉 ТЕКУЩИЕ АКЦИИ:")
        for promo_id, description in self.promotions.items():
            print(f"• {description}")

    def run_interactive_mode(self):
        """
        Запуск интерактивного режима работы ассистента
        """
        self.clear_screen()
        print("=" * 70)
        print("🤖 ДЕМО-АССИСТЕНТ-ПРОДАВЕЦ")
        print("=" * 70)
        print("Добро пожаловать в наш интернет-магазин электроники!")
        print("Я готов помочь вам с выбором товаров и ответить на все вопросы.")
        print("Напишите 'помощь' для просмотра доступных команд.")
        print("Напишите 'выход' для завершения работы.")
        print("=" * 70)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                    print("\n👋 Спасибо за обращение! До свидания!")
                    break
                
                if not user_input:
                    continue
                
                # Обработка специальных команд
                if user_input.lower() == 'помощь':
                    self.show_help()
                    continue
                elif user_input.lower() == 'акции' or user_input.lower() == 'скидки':
                    self.show_promotions()
                    continue
                elif 'показать' in user_input.lower():
                    if 'смартфон' in user_input.lower():
                        self.show_products('смартфоны')
                    elif 'ноутбук' in user_input.lower():
                        self.show_products('ноутбуки')
                    elif 'наушник' in user_input.lower():
                        self.show_products('наушники')
                    elif 'планшет' in user_input.lower():
                        self.show_products('планшеты')
                    elif 'аксессуар' in user_input.lower():
                        self.show_products('аксессуары')
                    else:
                        self.show_products()
                    continue
                elif user_input.lower().startswith('найти '):
                    query = user_input[6:]  # Убираем "найти "
                    results = self.search_products(query)
                    if results:
                        print(f"\n🔍 Результаты поиска для '{query}':")
                        for product in results:
                            print(f"• {product['name']} - {product['price']:,} ₽ ({product['category']})")
                    else:
                        print(f"\n❌ Товары по запросу '{query}' не найдены.")
                    continue
                elif user_input.lower().startswith('информация о '):
                    product_name = user_input[13:]  # Убираем "информация о "
                    product_info = self.get_product_info(product_name)
                    if product_info:
                        print(f"\n📋 ИНФОРМАЦИЯ О ТОВАРЕ:")
                        print(f"Название: {product_info['name']}")
                        print(f"Категория: {product_info['category']}")
                        print(f"Цена: {product_info['price']:,} ₽")
                        print(f"Описание: {product_info['description']}")
                        print(f"В наличии: {product_info['stock']} шт.")
                    else:
                        print(f"\n❌ Товар '{product_name}' не найден.")
                    continue
                
                print("\n🤖 Ассистент: ", end="", flush=True)
                
                # Получаем ответ от ассистента
                response = self.get_response(user_input)
                print(response)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Работа завершена пользователем. До свидания!")
                break
            except Exception as e:
                print(f"\n❌ Произошла ошибка: {e}")
                print("Попробуйте еще раз или напишите 'выход' для завершения.")

    def clear_screen(self):
        """
        Очистка экрана терминала
        """
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    Основная функция для запуска демо-ассистента
    """
    assistant = DemoSalesAssistant()
    assistant.run_interactive_mode()

if __name__ == "__main__":
    main()