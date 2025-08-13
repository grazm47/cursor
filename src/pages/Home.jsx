import React from 'react'
import { Link } from 'react-router-dom'
import { Calculator, Package, Shield, Truck, Users, Award } from 'lucide-react'
import './Home.css'

const Home = () => {
  const features = [
    {
      icon: <Shield />,
      title: 'Высокое качество',
      description: 'Оцинкованная проволока обеспечивает долговечность и устойчивость к коррозии'
    },
    {
      icon: <Package />,
      title: 'Широкий ассортимент',
      description: 'Различные размеры ячеек и толщины проволоки для любых задач'
    },
    {
      icon: <Truck />,
      title: 'Быстрая доставка',
      description: 'Доставляем по всей России в кратчайшие сроки'
    },
    {
      icon: <Calculator />,
      title: 'Удобный калькулятор',
      description: 'Рассчитайте необходимое количество сетки для вашего проекта'
    },
    {
      icon: <Users />,
      title: 'Профессиональная консультация',
      description: 'Наши специалисты помогут выбрать оптимальный вариант'
    },
    {
      icon: <Award />,
      title: 'Гарантия качества',
      description: 'Все изделия соответствуют ГОСТ и имеют сертификаты'
    }
  ]

  const applications = [
    {
      title: 'Заборы и ограждения',
      description: 'Надежная защита территории с эстетичным внешним видом'
    },
    {
      title: 'Строительство',
      description: 'Армирование бетона, штукатурки и других строительных материалов'
    },
    {
      title: 'Сельское хозяйство',
      description: 'Вольеры для животных, защита от грызунов'
    },
    {
      title: 'Ландшафтный дизайн',
      description: 'Оформление клумб, поддержка растений'
    }
  ]

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>Сетка рабица из оцинкованной проволоки</h1>
          <p>Надежное решение для заборов, строительства и сельского хозяйства</p>
          <div className="hero-buttons">
            <Link to="/calculator" className="btn btn-primary">
              Рассчитать стоимость
            </Link>
            <Link to="/catalog" className="btn btn-secondary">
              Посмотреть каталог
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section features">
        <div className="container">
          <h2 className="section-title">Почему выбирают нас</h2>
          <div className="grid grid-cols-3">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Applications Section */}
      <section className="section">
        <div className="container">
          <h2 className="section-title">Области применения</h2>
          <div className="grid grid-cols-2">
            {applications.map((app, index) => (
              <div key={index} className="card application-card">
                <h3>{app.title}</h3>
                <p>{app.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section cta-section">
        <div className="container">
          <div className="card cta-card">
            <h2>Готовы начать проект?</h2>
            <p>Наши специалисты помогут подобрать оптимальное решение для ваших задач</p>
            <div className="cta-buttons">
              <Link to="/contact" className="btn btn-primary">
                Получить консультацию
              </Link>
              <a href="tel:+78001234567" className="btn btn-secondary">
                Позвонить сейчас
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home