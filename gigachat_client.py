import requests
import json
import base64
import uuid
import time
from typing import Dict, List, Optional
import urllib3

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GigaChatClient:
    """Клиент для работы с API Гигачат"""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API ключ не может быть пустым")
        
        self.api_key = api_key
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires_at = None
        self.model = "GigaChat"
        self.max_retries = 3
        self.timeout = 30
        
    def _get_access_token(self) -> str:
        """Получение токена доступа"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self.api_key}"
        }
        
        data = {"scope": "GIGACHAT_API_PERS"}
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url, 
                    headers=headers, 
                    data=data, 
                    verify=False,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    # Сохраняем время истечения токена (обычно 30 минут)
                    self.token_expires_at = time.time() + token_data.get("expires_in", 1800)
                    return token_data["access_token"]
                elif response.status_code == 401:
                    raise Exception("Неверный API ключ. Проверьте правильность ключа.")
                elif response.status_code == 429:
                    raise Exception("Превышен лимит запросов. Попробуйте позже.")
                else:
                    raise Exception(f"Ошибка авторизации: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectTimeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Экспоненциальная задержка
                    continue
                raise Exception("Таймаут подключения к серверу Гигачат")
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception("Ошибка подключения к серверу Гигачат")
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"Ошибка сети: {str(e)}")
        
        raise Exception("Не удалось получить токен доступа после нескольких попыток")
    
    def _is_token_expired(self) -> bool:
        """Проверка истечения токена"""
        if not self.token_expires_at:
            return True
        # Обновляем токен за 5 минут до истечения
        return time.time() >= (self.token_expires_at - 300)
    
    def _ensure_token(self):
        """Проверка и обновление токена при необходимости"""
        if not self.access_token or self._is_token_expired():
            self.access_token = self._get_access_token()
    
    def _validate_message(self, message: str) -> None:
        """Валидация входящего сообщения"""
        if not message or not message.strip():
            raise ValueError("Сообщение не может быть пустым")
        
        if len(message) > 8000:  # Примерный лимит для Гигачат
            raise ValueError("Сообщение слишком длинное (максимум 8000 символов)")
    
    def send_message(self, message: str, conversation_history: List[Dict] = None) -> str:
        """
        Отправка сообщения в Гигачат
        
        Args:
            message: Текст сообщения
            conversation_history: История разговора (опционально)
            
        Returns:
            Ответ от Гигачат
        """
        # Валидация входных данных
        self._validate_message(message)
        
        for attempt in range(self.max_retries):
            try:
                self._ensure_token()
                
                url = f"{self.base_url}/chat/completions"
                
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.access_token}"
                }
                
                # Подготовка сообщений
                messages = []
                
                # Добавляем системное сообщение с контекстом продавца
                system_message = {
                    "role": "system",
                    "content": """Ты - дружелюбный и знающий ассистент-продавец в магазине электроники. 
                    Твоя задача:
                    1. Помогать покупателям выбрать подходящие товары
                    2. Отвечать на вопросы о характеристиках и функциях товаров
                    3. Предлагать альтернативы и сравнивать товары
                    4. Быть вежливым и терпеливым
                    5. Если не знаешь точной информации, честно об этом говори
                    6. Давать практические советы по использованию техники
                    7. Учитывать бюджет покупателя
                    
                    Отвечай на русском языке, будь дружелюбным и профессиональным.
                    Старайся быть кратким, но информативным."""
                }
                messages.append(system_message)
                
                # Добавляем историю разговора если есть
                if conversation_history:
                    # Ограничиваем историю для экономии токенов
                    recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
                    messages.extend(recent_history)
                
                # Добавляем текущее сообщение пользователя
                messages.append({"role": "user", "content": message})
                
                data = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
                
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=data, 
                    verify=False,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        content = response_data["choices"][0]["message"]["content"]
                        if content:
                            return content.strip()
                        else:
                            return "Извините, получен пустой ответ от ассистента."
                    else:
                        return "Извините, не удалось получить ответ от ассистента."
                        
                elif response.status_code == 401:
                    # Токен истек, попробуем обновить
                    self.access_token = None
                    if attempt < self.max_retries - 1:
                        continue
                    raise Exception("Ошибка авторизации. Проверьте API ключ.")
                    
                elif response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(5)  # Ждем перед повторной попыткой
                        continue
                    raise Exception("Превышен лимит запросов к API. Попробуйте позже.")
                    
                elif response.status_code >= 500:
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise Exception("Внутренняя ошибка сервера Гигачат. Попробуйте позже.")
                    
                else:
                    error_text = response.text if response.text else "Неизвестная ошибка"
                    raise Exception(f"Ошибка API Гигачат ({response.status_code}): {error_text}")
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception("Таймаут запроса к серверу Гигачат")
                
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception("Ошибка подключения к серверу Гигачат")
                
            except ValueError as e:
                # Не повторяем при ошибках валидации
                raise e
                
            except Exception as e:
                if attempt < self.max_retries - 1 and "API ключ" not in str(e):
                    time.sleep(2 ** attempt)
                    continue
                raise e
        
        raise Exception("Не удалось получить ответ после нескольких попыток")