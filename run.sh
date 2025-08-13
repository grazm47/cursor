#!/bin/bash

# Скрипт для запуска ассистента-продавца

echo "🛍️  Запуск ассистента-продавца с Гигачат..."
echo "════════════════════════════════════════════"

# Проверяем, установлен ли Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.7 или выше."
    exit 1
fi

# Проверяем существование requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден."
    exit 1
fi

# Проверяем существование .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден. Создайте файл .env с API ключом Гигачат."
    echo "   Формат: GIGACHAT_API_KEY=ваш_api_ключ"
    exit 1
fi

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости если нужно
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt --quiet

# Проверяем основные файлы
if [ ! -f "sales_assistant.py" ]; then
    echo "❌ Файл sales_assistant.py не найден."
    exit 1
fi

if [ ! -f "gigachat_client.py" ]; then
    echo "❌ Файл gigachat_client.py не найден."
    exit 1
fi

echo "✅ Все готово! Запускаем ассистента..."
echo ""

# Запускаем ассистента
python sales_assistant.py