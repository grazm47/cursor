import React, { useState } from 'react'
import { Package, Star, Filter, Search } from 'lucide-react'
import './Catalog.css'

const Catalog = () => {
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const products = [
    {
      id: 1,
      name: 'Сетка рабица 25x25 мм',
      description: 'Мелкая ячейка для защиты от мелких животных и птиц',
      meshSize: '25x25',
      wireDiameter: '1.6',
      price: 120,
      image: '🔲',
      category: 'fine',
      features: ['Защита от птиц', 'Декоративное ограждение', 'Вольеры для мелких животных']
    },
    {
      id: 2,
      name: 'Сетка рабица 35x35 мм',
      description: 'Универсальная сетка для заборов и ограждений',
      meshSize: '35x35',
      wireDiameter: '2.0',
      price: 100,
      image: '🔲',
      category: 'universal',
      features: ['Универсальное применение', 'Заборы', 'Ограждения']
    },
    {
      id: 3,
      name: 'Сетка рабица 50x50 мм',
      description: 'Стандартная сетка для большинства применений',
      meshSize: '50x50',
      wireDiameter: '2.0',
      price: 85,
      image: '🔲',
      category: 'standard',
      features: ['Стандартное применение', 'Заборы', 'Строительство']
    },
    {
      id: 4,
      name: 'Сетка рабица 75x75 мм',
      description: 'Крупная ячейка для экономичных решений',
      meshSize: '75x75',
      wireDiameter: '2.5',
      price: 70,
      image: '🔲',
      category: 'large',
      features: ['Экономичное решение', 'Временные ограждения', 'Строительные площадки']
    },
    {
      id: 5,
      name: 'Сетка рабица 100x100 мм',
      description: 'Очень крупная ячейка для специальных применений',
      meshSize: '100x100',
      wireDiameter: '3.0',
      price: 60,
      image: '🔲',
      category: 'extra-large',
      features: ['Специальные применения', 'Защита от крупных животных', 'Промышленное использование']
    },
    {
      id: 6,
      name: 'Сетка рабица усиленная',
      description: 'Усиленная сетка с толстой проволокой',
      meshSize: '50x50',
      wireDiameter: '3.0',
      price: 110,
      image: '🔲',
      category: 'reinforced',
      features: ['Повышенная прочность', 'Защитные ограждения', 'Промышленные объекты']
    }
  ]

  const categories = [
    { value: 'all', label: 'Все типы' },
    { value: 'fine', label: 'Мелкая ячейка' },
    { value: 'universal', label: 'Универсальная' },
    { value: 'standard', label: 'Стандартная' },
    { value: 'large', label: 'Крупная ячейка' },
    { value: 'extra-large', label: 'Очень крупная' },
    { value: 'reinforced', label: 'Усиленная' }
  ]

  const filteredProducts = products.filter(product => {
    const matchesFilter = filter === 'all' || product.category === filter
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesFilter && matchesSearch
  })

  return (
    <div className="catalog-page">
      <div className="container">
        <div className="catalog-header">
          <Package size={48} className="catalog-icon" />
          <h1>Каталог сетки рабицы</h1>
          <p>Выберите подходящий тип сетки для ваших задач</p>
        </div>

        <div className="catalog-filters">
          <div className="search-box">
            <Search size={20} />
            <input
              type="text"
              placeholder="Поиск по названию или описанию..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input"
            />
          </div>

          <div className="filter-buttons">
            {categories.map(category => (
              <button
                key={category.value}
                onClick={() => setFilter(category.value)}
                className={`filter-btn ${filter === category.value ? 'active' : ''}`}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>

        <div className="products-grid">
          {filteredProducts.map(product => (
            <div key={product.id} className="product-card">
              <div className="product-image">
                <span className="product-icon">{product.image}</span>
              </div>
              
              <div className="product-info">
                <h3>{product.name}</h3>
                <p className="product-description">{product.description}</p>
                
                <div className="product-specs">
                  <div className="spec">
                    <span>Ячейка:</span>
                    <strong>{product.meshSize} мм</strong>
                  </div>
                  <div className="spec">
                    <span>Проволока:</span>
                    <strong>{product.wireDiameter} мм</strong>
                  </div>
                </div>

                <div className="product-features">
                  {product.features.map((feature, index) => (
                    <span key={index} className="feature-tag">
                      {feature}
                    </span>
                  ))}
                </div>

                <div className="product-price">
                  <span className="price">{product.price} ₽/м²</span>
                  <div className="product-actions">
                    <button className="btn btn-primary">
                      <Package size={16} />
                      Заказать
                    </button>
                    <button className="btn btn-secondary">
                      Подробнее
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="no-results">
            <h3>Товары не найдены</h3>
            <p>Попробуйте изменить параметры поиска или фильтрации</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Catalog