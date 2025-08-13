#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import base64
import time
from typing import Optional, Dict, Any

class GigaChatSalesAssistant:
    def __init__(self, api_key: str):
        """
        Инициализация ассистента-продавца с API ключом GigaChat
        
        Args:
            api_key (str): API ключ для GigaChat
        """
        self.api_key = api_key
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires_at = 0
        
        # Системный промпт для ассистента-продавца
        self.system_prompt = """Ты - профессиональный ассистент-продавец в интернет-магазине. 
Твоя задача - помогать покупателям с выбором товаров, отвечать на их вопросы и способствовать совершению покупок.

Твои основные функции:
1. Приветствовать покупателей и предлагать помощь
2. Отвечать на вопросы о товарах, их характеристиках, ценах и наличии
3. Помогать с выбором товаров на основе потребностей покупателя
4. Информировать о акциях, скидках и специальных предложениях
5. Помогать с оформлением заказа
6. Отвечать на вопросы о доставке, оплате и возврате

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
                verify=False  # Отключаем проверку SSL для тестирования
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.token_expires_at = time.time() + token_data["expires_in"] - 60  # Обновляем за минуту до истечения
            
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении access token: {e}")
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

    def run_interactive_mode(self):
        """
        Запуск интерактивного режима работы ассистента
        """
        print("=" * 60)
        print("🤖 АССИСТЕНТ-ПРОДАВЕЦ")
        print("=" * 60)
        print("Добро пожаловать! Я готов помочь вам с выбором товаров.")
        print("Напишите 'выход' для завершения работы.")
        print("=" * 60)
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                    print("\n👋 Спасибо за обращение! До свидания!")
                    break
                
                if not user_input:
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

def main():
    """
    Основная функция для запуска ассистента
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
    assistant = GigaChatSalesAssistant(decoded_key)
    assistant.run_interactive_mode()

if __name__ == "__main__":
    main()