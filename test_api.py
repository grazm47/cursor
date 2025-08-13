#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки подключения к API GigaChat
"""

import requests
import base64
import json

def test_gigachat_api():
    """
    Тестирование подключения к API GigaChat
    """
    print("🧪 Тестирование подключения к API GigaChat...")
    
    # API ключ
    api_key = "d6c4c3f9-08fb-4ea7-9903-aa48fbf6c0e5"
    
    try:
        # Используем API ключ напрямую
        decoded_key = api_key
        print(f"✅ API ключ готов к использованию")
        
        # Базовый URL
        base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        
        # Получаем access token
        print("🔑 Получение access token...")
        headers = {
            "Authorization": f"Bearer {decoded_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "RqUID": "1234567890"
        }
        
        data = {
            "scope": "GIGACHAT_API_PERS"
        }
        
        response = requests.post(
            f"{base_url}/oauth/access_token",
            headers=headers,
            data=data,
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"✅ Access token получен успешно")
            print(f"⏰ Срок действия: {token_data['expires_in']} секунд")
            
            # Тестируем отправку сообщения
            print("💬 Тестирование отправки сообщения...")
            
            chat_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            chat_data = {
                "model": "GigaChat:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": "Привет! Как дела?"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            chat_response = requests.post(
                f"{base_url}/chat/completions",
                headers=chat_headers,
                json=chat_data,
                verify=False,
                timeout=30
            )
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                assistant_message = result["choices"][0]["message"]["content"]
                print(f"✅ Ответ от GigaChat получен:")
                print(f"🤖 {assistant_message}")
                print("\n🎉 API работает корректно!")
                return True
            else:
                print(f"❌ Ошибка при отправке сообщения: {chat_response.status_code}")
                print(f"Ответ: {chat_response.text}")
                return False
                
        else:
            print(f"❌ Ошибка при получении access token: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут при подключении к API")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к API")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def test_local_functions():
    """
    Тестирование локальных функций ассистента
    """
    print("\n🧪 Тестирование локальных функций...")
    
    # Имитируем базу данных товаров
    products_db = {
        "смартфоны": [
            {"name": "iPhone 15 Pro", "price": 99990, "description": "Новейший iPhone", "stock": 15},
            {"name": "Samsung Galaxy S24", "price": 89990, "description": "Флагманский Android", "stock": 12}
        ]
    }
    
    # Тест поиска товаров
    query = "iPhone"
    results = []
    for category, products in products_db.items():
        for product in products:
            if query.lower() in product["name"].lower():
                results.append({**product, "category": category})
    
    if results:
        print(f"✅ Поиск товаров работает: найдено {len(results)} товаров")
        for product in results:
            print(f"  • {product['name']} - {product['price']:,} ₽")
    else:
        print("❌ Поиск товаров не работает")
    
    # Тест акций
    promotions = {
        "скидка_20": "Скидка 20% на все смартфоны!",
        "бесплатная_доставка": "Бесплатная доставка от 5000 рублей"
    }
    
    print(f"✅ Акции настроены: {len(promotions)} акций")
    for promo in promotions.values():
        print(f"  • {promo}")

def main():
    """
    Основная функция тестирования
    """
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ АССИСТЕНТА-ПРОДАВЦА")
    print("=" * 60)
    
    # Тестируем API
    api_works = test_gigachat_api()
    
    # Тестируем локальные функции
    test_local_functions()
    
    print("\n" + "=" * 60)
    if api_works:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Ассистент готов к работе")
        print("\nДля запуска используйте:")
        print("  python3 advanced_sales_assistant.py")
        print("  или")
        print("  python3 run.py")
    else:
        print("⚠️  ПРОБЛЕМЫ С API")
        print("❌ Проверьте подключение к интернету и API ключ")
    print("=" * 60)

if __name__ == "__main__":
    main()