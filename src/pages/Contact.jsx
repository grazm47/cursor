import React, { useState } from 'react'
import { Phone, Mail, MapPin, Clock, Send, MessageCircle } from 'lucide-react'
import './Contact.css'

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
    product: ''
  })

  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Здесь будет логика отправки формы
    console.log('Form submitted:', formData)
    setIsSubmitted(true)
    setFormData({
      name: '',
      email: '',
      phone: '',
      message: '',
      product: ''
    })
  }

  const contactInfo = [
    {
      icon: <Phone />,
      title: 'Телефон',
      value: '8 800 123-45-67',
      link: 'tel:+78001234567',
      description: 'Бесплатный звонок по России'
    },
    {
      icon: <Mail />,
      title: 'Email',
      value: 'info@rabitsa.ru',
      link: 'mailto:info@rabitsa.ru',
      description: 'Напишите нам письмо'
    },
    {
      icon: <MapPin />,
      title: 'Адрес',
      value: 'г. Москва, ул. Примерная, 123',
      link: '#',
      description: 'Наш офис и склад'
    },
    {
      icon: <Clock />,
      title: 'Режим работы',
      value: 'Пн-Пт: 9:00-18:00',
      link: '#',
      description: 'Сб-Вс: 10:00-16:00'
    }
  ]

  const products = [
    'Сетка рабица 25x25 мм',
    'Сетка рабица 35x35 мм',
    'Сетка рабица 50x50 мм',
    'Сетка рабица 75x75 мм',
    'Сетка рабица 100x100 мм',
    'Сетка рабица усиленная',
    'Другое'
  ]

  return (
    <div className="contact-page">
      <div className="container">
        <div className="contact-header">
          <MessageCircle size={48} className="contact-icon" />
          <h1>Свяжитесь с нами</h1>
          <p>Получите профессиональную консультацию по выбору сетки рабицы</p>
        </div>

        <div className="contact-content">
          <div className="contact-info">
            <div className="card">
              <h2>Контактная информация</h2>
              <div className="contact-list">
                {contactInfo.map((info, index) => (
                  <div key={index} className="contact-item">
                    <div className="contact-icon-small">
                      {info.icon}
                    </div>
                    <div className="contact-details">
                      <h3>{info.title}</h3>
                      <a href={info.link} className="contact-value">
                        {info.value}
                      </a>
                      <p>{info.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <h2>Почему обращаться к нам</h2>
              <ul className="benefits-list">
                <li>Более 10 лет на рынке</li>
                <li>Собственное производство</li>
                <li>Гарантия качества</li>
                <li>Быстрая доставка</li>
                <li>Профессиональная консультация</li>
                <li>Гибкая система скидок</li>
              </ul>
            </div>
          </div>

          <div className="contact-form">
            <div className="card">
              <h2>Отправить заявку</h2>
              
              {isSubmitted ? (
                <div className="success-message">
                  <h3>Спасибо за заявку!</h3>
                  <p>Мы свяжемся с вами в ближайшее время для уточнения деталей.</p>
                  <button 
                    onClick={() => setIsSubmitted(false)}
                    className="btn btn-primary"
                  >
                    Отправить еще одну заявку
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label htmlFor="name">Ваше имя *</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      className="input"
                      placeholder="Введите ваше имя"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="input"
                      placeholder="your@email.com"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="phone">Телефон *</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="input"
                      placeholder="+7 (999) 123-45-67"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="product">Интересующий товар</label>
                    <select
                      id="product"
                      name="product"
                      value={formData.product}
                      onChange={handleInputChange}
                      className="input"
                    >
                      <option value="">Выберите товар</option>
                      {products.map((product, index) => (
                        <option key={index} value={product}>
                          {product}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="message">Сообщение</label>
                    <textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      className="input"
                      rows="4"
                      placeholder="Опишите ваши потребности или задайте вопрос..."
                    />
                  </div>

                  <button type="submit" className="btn btn-primary">
                    <Send size={20} />
                    Отправить заявку
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Contact