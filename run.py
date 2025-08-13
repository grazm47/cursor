#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для запуска ассистента-продавца
"""

import sys
import os

def main():
    print("🤖 АССИСТЕНТ-ПРОДАВЕЦ")
    print("=" * 40)
    print("Выберите версию для запуска:")
    print("1. Демо-ассистент (работает локально)")
    print("2. Базовый ассистент с GigaChat API")
    print("3. Расширенный ассистент с GigaChat API")
    print("4. Тест API GigaChat")
    print("5. Выход")
    print("=" * 40)
    
    while True:
        try:
            choice = input("Введите номер (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Запуск демо-ассистента...")
                os.system("python3 demo_assistant.py")
                break
            elif choice == "2":
                print("\n🚀 Запуск базового ассистента с API...")
                os.system("python3 sales_assistant.py")
                break
            elif choice == "3":
                print("\n🚀 Запуск расширенного ассистента с API...")
                os.system("python3 advanced_sales_assistant.py")
                break
            elif choice == "4":
                print("\n🧪 Тестирование API GigaChat...")
                os.system("python3 test_api.py")
                break
            elif choice == "5":
                print("\n👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Введите 1, 2, 3, 4 или 5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()