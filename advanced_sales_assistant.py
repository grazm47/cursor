#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import base64
import time
import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime

class AdvancedGigaChatSalesAssistant:
    def __init__(self, api_key: str):
        """
        Инициализация расширенного ассистента-продавца с API ключом GigaChat
        
        Args:
            api_key (str): API ключ для GigaChat
        """
        self.api_key = api_key
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires_at = 0
        
        # База данных товаров (в реальном проекте это была бы база данных)
        self.products_db = {
            "смартфоны": [
                {"name": "iPhone 15 Pro", "price": 99990, "description": "Новейший iPhone с титановым корпусом", "stock": 15},
                {"name": "Samsung Galaxy S24", "price": 89990, "description": "Флагманский Android смартфон", "stock": 12},
                {"name": "Xiaomi 14", "price": 69990, "description": "Отличное соотношение цена-качество", "stock": 20}
            ],
            "ноутбуки": [
                {"name": "MacBook Pro 14", "price": 199990, "description": "Мощный ноутбук для профессионалов", "stock": 8},
                {"name": "Dell XPS 13", "price": 149990, "description": "Ультрабук премиум класса", "stock": 10},
                {"name": "Lenovo ThinkPad X1", "price": 179990, "description": "Бизнес-ноутбук высшего класса", "stock": 6}
            ],
            "наушники": [
                {"name": "AirPods Pro 2", "price": 24990, "description": "Беспроводные наушники с шумоподавлением", "stock": 25},
                {"name": "Sony WH-1000XM5", "price": 39990, "description": "Лучшие накладные наушники", "stock": 18},
                {"name": "Samsung Galaxy Buds2", "price": 15990, "description": "Компактные TWS наушники", "stock": 30}
            ]
        }
        
        # Акции и скидки
        self.promotions = {
            "скидка_20": "Скидка 20% на все смартфоны до конца недели!",
            "бесплатная_доставка": "Бесплатная доставка при заказе от 5000 рублей",
            "подарок": "При покупке ноутбука - бесплатные наушники в подарок!"
        }
        
        # Системный промпт для ассистента-продавца
        self.system_prompt = """Ты - профессиональный ассистент-продавец в интернет-магазине электроники. 
Твоя задача - помогать покупателям с выбором товаров, отвечать на их вопросы и способствовать совершению покупок.

Твои основные функции:
1. Приветствовать покупателей и предлагать помощь
2. Отвечать на вопросы о товарах, их характеристиках, ценах и наличии
3. Помогать с выбором товаров на основе потребностей покупателя
4. Информировать о акциях, скидках и специальных предложениях
5. Помогать с оформлением заказа
6. Отвечать на вопросы о доставке, оплате и возврате

Доступные категории товаров:
- Смартфоны (iPhone, Samsung, Xiaomi)
- Ноутбуки (MacBook, Dell, Lenovo)
- Наушники (AirPods, Sony, Samsung)

Акции:
- Скидка 20% на все смартфоны
- Бесплатная доставка от 5000 рублей
- Подарок при покупке ноутбука

Будь вежливым, дружелюбным и профессиональным. Всегда старайся быть полезным и помогать покупателю найти то, что ему нужно."""

    def _get_access_token(self) -> str:
        """
        Получение access token для API GigaChat
        
        Returns:
            str: Access token
        """
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "RqUID": "1234567890"
        }
        
        data = {
            "scope": "GIGACHAT_API_PERS"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/oauth/access_token",
                headers=headers,
                data=data,
                verify=False
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.token_expires_at = time.time() + token_data["expires_in"] - 60
            
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении access token: {e}")
            return None

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

    def send_message(self, message: str, conversation_history: Optional[list] = None) -> str:
        """
        Отправка сообщения в GigaChat и получение ответа
        
        Args:
            message (str): Сообщение пользователя
            conversation_history (list, optional): История разговора
            
        Returns:
            str: Ответ от ассистента
        """
        access_token = self._get_access_token()
        if not access_token:
            return "Извините, не удалось подключиться к сервису. Попробуйте позже."
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Формируем сообщения для API
        messages = []
        
        # Добавляем системный промпт
        messages.append({
            "role": "system",
            "content": self.system_prompt
        })
        
        # Добавляем историю разговора
        if conversation_history:
            messages.extend(conversation_history)
        
        # Добавляем текущее сообщение пользователя
        messages.append({
            "role": "user",
            "content": message
        })
        
        data = {
            "model": "GigaChat:latest",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                verify=False
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке сообщения: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса. Попробуйте еще раз."

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
            print(f"\n📱 {category.upper()}:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product['name']} - {product['price']:,} ₽")
                print(f"   {product['description']}")
                print(f"   В наличии: {product['stock']} шт.")
                print()
        else:
            print("\n📦 ВСЕ ТОВАРЫ:")
            for category, products in self.products_db.items():
                print(f"\n{category.upper()}:")
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
        print("🤖 РАСШИРЕННЫЙ АССИСТЕНТ-ПРОДАВЕЦ")
        print("=" * 70)
        print("Добро пожаловать в наш интернет-магазин электроники!")
        print("Я готов помочь вам с выбором товаров и ответить на все вопросы.")
        print("Напишите 'помощь' для просмотра доступных команд.")
        print("Напишите 'выход' для завершения работы.")
        print("=" * 70)
        
        conversation_history = []
        
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
                response = self.send_message(user_input, conversation_history)
                print(response)
                
                # Обновляем историю разговора
                conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Ограничиваем историю разговора (последние 10 сообщений)
                if len(conversation_history) > 10:
                    conversation_history = conversation_history[-10:]
                    
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
    Основная функция для запуска расширенного ассистента
    """
    # API ключ GigaChat (закодированный в base64)
    api_key = "ZDZjNGMzZjktMDhmYi00ZWE3LTk5MDMtYWE0OGZiZjZjMGU1OmMyOTk0MmE0LWM5NjgtNDEzZi05NjEzLTg0MWIxNTI2ZDAxMQ=="
    
    # Декодируем API ключ
    try:
        decoded_key = base64.b64decode(api_key).decode('utf-8')
    except Exception as e:
        print(f"Ошибка при декодировании API ключа: {e}")
        return
    
    # Создаем и запускаем ассистента
    assistant = AdvancedGigaChatSalesAssistant(decoded_key)
    assistant.run_interactive_mode()

if __name__ == "__main__":
    main()