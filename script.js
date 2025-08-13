// Данные каталога сетки рабица
const catalogData = [
    {
        id: 1,
        name: "Сетка рабица 50×50мм",
        price: 120,
        specs: [
            "Размер ячейки: 50×50 мм",
            "Диаметр проволоки: 1.8 мм",
            "Высота рулона: 1.5 м",
            "Длина рулона: 10 м",
            "Покрытие: оцинковка"
        ],
        image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150' viewBox='0 0 200 150'%3E%3Crect width='200' height='150' fill='%23f0f0f0'/%3E%3Cg stroke='%234a7c59' stroke-width='2' fill='none'%3E%3Cpath d='M0 0L200 0M0 25L200 25M0 50L200 50M0 75L200 75M0 100L200 100M0 125L200 125M0 150L200 150'/%3E%3Cpath d='M0 0L0 150M25 0L25 150M50 0L50 150M75 0L75 150M100 0L100 150M125 0L125 150M150 0L150 150M175 0L175 150M200 0L200 150'/%3E%3C/g%3E%3C/svg%3E"
    },
    {
        id: 2,
        name: "Сетка рабица 35×35мм",
        price: 140,
        specs: [
            "Размер ячейки: 35×35 мм",
            "Диаметр проволоки: 1.8 мм",
            "Высота рулона: 1.5 м",
            "Длина рулона: 10 м",
            "Покрытие: оцинковка"
        ],
        image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150' viewBox='0 0 200 150'%3E%3Crect width='200' height='150' fill='%23f0f0f0'/%3E%3Cg stroke='%234a7c59' stroke-width='2' fill='none'%3E%3Cpath d='M0 0L200 0M0 18L200 18M0 36L200 36M0 54L200 54M0 72L200 72M0 90L200 90M0 108L200 108M0 126L200 126M0 144L200 144'/%3E%3Cpath d='M0 0L0 150M18 0L18 150M36 0L36 150M54 0L54 150M72 0L72 150M90 0L90 150M108 0L108 150M126 0L126 150M144 0L144 150M162 0L162 150M180 0L180 150M198 0L198 150'/%3E%3C/g%3E%3C/svg%3E"
    },
    {
        id: 3,
        name: "Сетка рабица 25×25мм",
        price: 180,
        specs: [
            "Размер ячейки: 25×25 мм",
            "Диаметр проволоки: 1.6 мм",
            "Высота рулона: 1.5 м",
            "Длина рулона: 10 м",
            "Покрытие: оцинковка"
        ],
        image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150' viewBox='0 0 200 150'%3E%3Crect width='200' height='150' fill='%23f0f0f0'/%3E%3Cg stroke='%234a7c59' stroke-width='1.5' fill='none'%3E%3Cpath d='M0 0L200 0M0 12L200 12M0 24L200 24M0 36L200 36M0 48L200 48M0 60L200 60M0 72L200 72M0 84L200 84M0 96L200 96M0 108L200 108M0 120L200 120M0 132L200 132M0 144L200 144'/%3E%3Cpath d='M0 0L0 150M12 0L12 150M24 0L24 150M36 0L36 150M48 0L48 150M60 0L60 150M72 0L72 150M84 0L84 150M96 0L96 150M108 0L108 150M120 0L120 150M132 0L132 150M144 0L144 150M156 0L156 150M168 0L168 150M180 0L180 150M192 0L192 150'/%3E%3C/g%3E%3C/svg%3E"
    },
    {
        id: 4,
        name: "Сетка рабица 60×60мм",
        price: 100,
        specs: [
            "Размер ячейки: 60×60 мм",
            "Диаметр проволоки: 2.0 мм",
            "Высота рулона: 1.5 м",
            "Длина рулона: 10 м",
            "Покрытие: оцинковка"
        ],
        image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150' viewBox='0 0 200 150'%3E%3Crect width='200' height='150' fill='%23f0f0f0'/%3E%3Cg stroke='%234a7c59' stroke-width='2.5' fill='none'%3E%3Cpath d='M0 0L200 0M0 30L200 30M0 60L200 60M0 90L200 90M0 120L200 120M0 150L200 150'/%3E%3Cpath d='M0 0L0 150M30 0L30 150M60 0L60 150M90 0L90 150M120 0L120 150M150 0L150 150M180 0L180 150'/%3E%3C/g%3E%3C/svg%3E"
    }
];

// Ценообразование
const pricing = {
    25: { basePrice: 180, wireFactor: { 1.4: 0.9, 1.6: 1.0, 1.8: 1.1, 2.0: 1.2, 2.5: 1.4 } },
    35: { basePrice: 140, wireFactor: { 1.4: 0.9, 1.6: 1.0, 1.8: 1.1, 2.0: 1.2, 2.5: 1.4 } },
    40: { basePrice: 130, wireFactor: { 1.4: 0.9, 1.6: 1.0, 1.8: 1.1, 2.0: 1.2, 2.5: 1.4 } },
    50: { basePrice: 120, wireFactor: { 1.4: 0.9, 1.6: 1.0, 1.8: 1.1, 2.0: 1.2, 2.5: 1.4 } },
    60: { basePrice: 100, wireFactor: { 1.4: 0.9, 1.6: 1.0, 1.8: 1.1, 2.0: 1.2, 2.5: 1.4 } }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    renderCatalog();
    calculatePrice();
    
    // Добавляем обработчики событий для калькулятора
    document.getElementById('meshSize').addEventListener('change', calculatePrice);
    document.getElementById('height').addEventListener('change', calculatePrice);
    document.getElementById('length').addEventListener('input', calculatePrice);
    document.getElementById('wireSize').addEventListener('change', calculatePrice);
    
    // Обработчик для Enter в чате
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

// Рендеринг каталога
function renderCatalog() {
    const catalogGrid = document.getElementById('catalogGrid');
    catalogGrid.innerHTML = '';
    
    catalogData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'catalog-card';
        card.innerHTML = `
            <img src="${item.image}" alt="${item.name}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
            <h3>${item.name}</h3>
            <div class="price">от ${item.price} ₽/м²</div>
            <ul class="specs">
                ${item.specs.map(spec => `<li>${spec}</li>`).join('')}
            </ul>
            <button class="btn-primary" onclick="selectProduct(${item.id})">Выбрать</button>
        `;
        catalogGrid.appendChild(card);
    });
}

// Выбор продукта из каталога
function selectProduct(productId) {
    const product = catalogData.find(p => p.id === productId);
    if (product) {
        // Заполняем калькулятор данными выбранного продукта
        const meshSize = product.name.match(/(\d+)×\d+мм/);
        if (meshSize) {
            document.getElementById('meshSize').value = meshSize[1];
        }
        
        // Прокручиваем к калькулятору
        scrollToSection('calculator');
        calculatePrice();
    }
}

// Калькулятор стоимости
function calculatePrice() {
    const meshSize = parseInt(document.getElementById('meshSize').value);
    const height = parseFloat(document.getElementById('height').value);
    const length = parseFloat(document.getElementById('length').value);
    const wireSize = parseFloat(document.getElementById('wireSize').value);
    
    // Расчет площади
    const area = height * length;
    
    // Получение базовой цены и коэффициента
    const priceData = pricing[meshSize];
    const basePrice = priceData.basePrice;
    const wireFactor = priceData.wireFactor[wireSize];
    
    // Расчет цены за м²
    const pricePerSqm = Math.round(basePrice * wireFactor);
    
    // Общая стоимость
    const totalPrice = Math.round(area * pricePerSqm);
    
    // Обновление результатов
    document.getElementById('area').textContent = `${area.toFixed(1)} м²`;
    document.getElementById('pricePerSqm').textContent = `${pricePerSqm} ₽`;
    document.getElementById('totalPrice').textContent = `${totalPrice.toLocaleString()} ₽`;
    
    // Сохраняем данные для заказа
    window.currentCalculation = {
        meshSize,
        height,
        length,
        wireSize,
        area,
        pricePerSqm,
        totalPrice
    };
}

// Открытие формы заказа
function openOrderForm() {
    const modal = document.getElementById('orderModal');
    const summary = document.getElementById('orderSummary');
    
    if (window.currentCalculation) {
        const calc = window.currentCalculation;
        summary.innerHTML = `
            <h4>Детали заказа:</h4>
            <p><strong>Размер ячейки:</strong> ${calc.meshSize}×${calc.meshSize} мм</p>
            <p><strong>Диаметр проволоки:</strong> ${calc.wireSize} мм</p>
            <p><strong>Размеры:</strong> ${calc.height}м × ${calc.length}м</p>
            <p><strong>Площадь:</strong> ${calc.area.toFixed(1)} м²</p>
            <p><strong>Стоимость:</strong> ${calc.totalPrice.toLocaleString()} ₽</p>
        `;
    }
    
    modal.style.display = 'flex';
}

// Закрытие модального окна
function closeOrderModal() {
    document.getElementById('orderModal').style.display = 'none';
}

// Отправка заказа
function submitOrder(event) {
    event.preventDefault();
    
    // Здесь будет отправка данных на сервер
    alert('Спасибо за заказ! Мы свяжемся с вами в ближайшее время.');
    closeOrderModal();
    
    // Очистка формы
    event.target.reset();
}

// Чат-бот
let chatHistory = [];

const chatResponses = {
    keywords: {
        'размер': 'У нас есть сетка с размерами ячеек: 25×25, 35×35, 40×40, 50×50, 60×60 мм. Какой размер вас интересует?',
        'цена': 'Цены начинаются от 100 ₽/м² для сетки 60×60 мм и до 180 ₽/м² для сетки 25×25 мм. Воспользуйтесь нашим калькулятором для точного расчета!',
        'доставка': 'Мы доставляем по Москве и области в течение 1-2 дней. Стоимость доставки зависит от объема заказа и расстояния.',
        'качество': 'Вся наша сетка изготавливается из оцинкованной проволоки с антикоррозийным покрытием. Гарантия до 5 лет!',
        'забор': 'Для забора рекомендуем сетку 50×50 мм с проволокой 1.8-2.0 мм. Это оптимальное соотношение цены и прочности.',
        'курятник': 'Для курятника подойдет сетка 25×25 или 35×35 мм - она не даст пройти мелким животным.',
        'вольер': 'Для вольера животных рекомендуем сетку 35×35 или 40×40 мм с проволокой 1.8-2.0 мм.',
        'дача': 'Для дачного участка популярна сетка 50×50 мм высотой 1.5-2.0 м. Хотите рассчитать стоимость?',
        'участок': 'Для ограждения участка подойдет сетка 50×50 или 60×60 мм. Какая площадь у вашего участка?',
        'высота': 'Доступная высота рулонов: 1.0, 1.2, 1.5, 1.8, 2.0 метра. Какая высота вам нужна?'
    },
    
    defaultResponses: [
        'Расскажите подробнее о ваших потребностях, и я помогу подобрать подходящую сетку рабица.',
        'Я могу помочь вам выбрать размер ячейки и рассчитать стоимость. Что именно вас интересует?',
        'Для лучшей консультации скажите, для какой цели нужна сетка: забор, вольер, курятник?',
        'Предлагаю воспользоваться нашим калькулятором стоимости или уточнить детали по телефону +7 (495) 123-45-67'
    ]
};

function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.style.display = chatContainer.style.display === 'none' || !chatContainer.style.display ? 'flex' : 'none';
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Добавляем сообщение пользователя
    addMessage(message, 'user');
    input.value = '';
    
    // Генерируем ответ бота
    setTimeout(() => {
        const response = generateBotResponse(message);
        addMessage(response, 'bot');
    }, 1000);
}

function addMessage(text, type) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    chatHistory.push({ text, type });
}

function generateBotResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Поиск ключевых слов
    for (const [keyword, response] of Object.entries(chatResponses.keywords)) {
        if (message.includes(keyword)) {
            return response;
        }
    }
    
    // Случайный ответ по умолчанию
    const randomIndex = Math.floor(Math.random() * chatResponses.defaultResponses.length);
    return chatResponses.defaultResponses[randomIndex];
}

// Прокрутка к секции
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('orderModal');
    if (event.target === modal) {
        closeOrderModal();
    }
}

// Плавная прокрутка для навигации
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
});

// Анимация появления элементов при прокрутке
function animateOnScroll() {
    const elements = document.querySelectorAll('.catalog-card, .about-card');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

window.addEventListener('scroll', animateOnScroll);

// Инициализация стилей для анимации
document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('.catalog-card, .about-card');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    animateOnScroll();
});