#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
import colorama
from colorama import Fore, Back, Style

from gigachat_client import GigaChatClient

# Инициализация colorama для цветного вывода
colorama.init(autoreset=True)

class SalesAssistant:
    """Главный класс ассистента-продавца"""
    
    def __init__(self):
        # Загружаем переменные окружения
        load_dotenv()
        
        # Получаем API ключ
        api_key = os.getenv("GIGACHAT_API_KEY")
        if not api_key:
            raise ValueError("API ключ Гигачат не найден в переменных окружения")
        
        # Инициализируем клиент Гигачат
        self.gigachat_client = GigaChatClient(api_key)
        
        # История разговора
        self.conversation_history: List[Dict] = []
        
        # Флаг работы приложения
        self.running = True
    
    def print_welcome(self):
        """Вывод приветственного сообщения"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🛍️  ДОБРО ПОЖАЛОВАТЬ В МАГАЗИН ЭЛЕКТРОНИКИ!")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}Я ваш персональный ассистент-продавец.")
        print(f"{Fore.GREEN}Я помогу вам:")
        print(f"{Fore.YELLOW}  • Выбрать подходящие товары")
        print(f"{Fore.YELLOW}  • Узнать характеристики и функции")
        print(f"{Fore.YELLOW}  • Сравнить различные модели")
        print(f"{Fore.YELLOW}  • Ответить на ваши вопросы")
        print(f"\n{Fore.MAGENTA}Команды управления:")
        print(f"{Fore.MAGENTA}  • 'выход' или 'quit' - завершить работу")
        print(f"{Fore.MAGENTA}  • 'очистить' или 'clear' - очистить историю")
        print(f"{Fore.MAGENTA}  • 'помощь' или 'help' - показать эту справку")
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def print_help(self):
        """Вывод справки"""
        print(f"\n{Fore.CYAN}📋 СПРАВКА ПО КОМАНДАМ:")
        print(f"{Fore.YELLOW}  • выход, quit, q - завершить работу")
        print(f"{Fore.YELLOW}  • очистить, clear, c - очистить историю разговора") 
        print(f"{Fore.YELLOW}  • помощь, help, h - показать эту справку")
        print(f"{Fore.GREEN}  • Любой другой текст - вопрос ассистенту")
        print(f"{Fore.CYAN}{'='*40}\n")
    
    def clear_history(self):
        """Очистка истории разговора"""
        self.conversation_history.clear()
        print(f"{Fore.GREEN}✅ История разговора очищена.\n")
    
    def process_user_command(self, user_input: str) -> bool:
        """
        Обработка команд пользователя
        
        Args:
            user_input: Ввод пользователя
            
        Returns:
            True если нужно продолжить работу, False если нужно выйти
        """
        user_input = user_input.strip().lower()
        
        # Команды выхода
        if user_input in ['выход', 'quit', 'q', 'exit']:
            print(f"{Fore.CYAN}👋 Спасибо за покупки! До свидания!")
            return False
        
        # Команды очистки истории
        elif user_input in ['очистить', 'clear', 'c']:
            self.clear_history()
            return True
        
        # Команды помощи
        elif user_input in ['помощь', 'help', 'h']:
            self.print_help()
            return True
        
        return True
    
    def get_user_input(self) -> str:
        """Получение ввода от пользователя"""
        try:
            print(f"{Fore.BLUE}💬 Вы: {Style.RESET_ALL}", end="")
            user_input = input().strip()
            return user_input
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 Работа завершена. До свидания!")
            return "quit"
        except EOFError:
            return "quit"
    
    def send_to_gigachat(self, message: str) -> str:
        """Отправка сообщения в Гигачат и получение ответа"""
        try:
            print(f"{Fore.YELLOW}🤖 Ассистент думает...")
            
            # Отправляем сообщение
            response = self.gigachat_client.send_message(
                message, 
                self.conversation_history
            )
            
            # Сохраняем в историю
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Ограничиваем историю (последние 10 сообщений)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response
            
        except Exception as e:
            error_msg = f"Извините, произошла ошибка: {str(e)}"
            print(f"{Fore.RED}❌ {error_msg}")
            return error_msg
    
    def run(self):
        """Основной цикл работы ассистента"""
        self.print_welcome()
        
        while self.running:
            try:
                # Получаем ввод пользователя
                user_input = self.get_user_input()
                
                # Проверяем на пустой ввод
                if not user_input:
                    continue
                
                # Обрабатываем команды
                if not self.process_user_command(user_input):
                    break
                
                # Если это не команда, отправляем в Гигачат
                if user_input.lower() not in ['выход', 'quit', 'q', 'exit', 
                                              'очистить', 'clear', 'c', 
                                              'помощь', 'help', 'h']:
                    
                    response = self.send_to_gigachat(user_input)
                    print(f"\n{Fore.GREEN}🤖 Ассистент: {Style.RESET_ALL}{response}\n")
                    print(f"{Fore.CYAN}{'-'*60}")
                
            except Exception as e:
                print(f"{Fore.RED}❌ Произошла неожиданная ошибка: {str(e)}")
                print(f"{Fore.YELLOW}Попробуйте еще раз или введите 'выход' для завершения работы.")


def main():
    """Главная функция"""
    try:
        assistant = SalesAssistant()
        assistant.run()
    except ValueError as e:
        print(f"{Fore.RED}❌ Ошибка конфигурации: {str(e)}")
        print(f"{Fore.YELLOW}Убедитесь, что API ключ указан в файле .env")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ Критическая ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()