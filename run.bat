@echo off
chcp 65001 >nul
echo 🛍️  Запуск ассистента-продавца с Гигачат...
echo ════════════════════════════════════════════

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Установите Python 3.7 или выше.
    pause
    exit /b 1
)

REM Проверяем существование requirements.txt
if not exist "requirements.txt" (
    echo ❌ Файл requirements.txt не найден.
    pause
    exit /b 1
)

REM Проверяем существование .env файла
if not exist ".env" (
    echo ❌ Файл .env не найден. Создайте файл .env с API ключом Гигачат.
    echo    Формат: GIGACHAT_API_KEY=ваш_api_ключ
    pause
    exit /b 1
)

REM Создаем виртуальное окружение если его нет
if not exist "venv" (
    echo 📦 Создаем виртуальное окружение...
    python -m venv venv
)

REM Активируем виртуальное окружение
echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate

REM Устанавливаем зависимости если нужно
echo 📦 Устанавливаем зависимости...
pip install -r requirements.txt --quiet

REM Проверяем основные файлы
if not exist "sales_assistant.py" (
    echo ❌ Файл sales_assistant.py не найден.
    pause
    exit /b 1
)

if not exist "gigachat_client.py" (
    echo ❌ Файл gigachat_client.py не найден.
    pause
    exit /b 1
)

echo ✅ Все готово! Запускаем ассистента...
echo.

REM Запускаем ассистента
python sales_assistant.py

pause