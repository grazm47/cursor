import React, { useState } from 'react'
import { Calculator as CalcIcon, Info, Package } from 'lucide-react'
import './Calculator.css'

const Calculator = () => {
  const [formData, setFormData] = useState({
    width: '',
    height: '',
    meshSize: '50x50',
    wireDiameter: '2.0',
    quantity: 1
  })

  const [result, setResult] = useState(null)

  const meshSizes = [
    { value: '25x25', label: '25x25 мм', price: 120 },
    { value: '35x35', label: '35x35 мм', price: 100 },
    { value: '50x50', label: '50x50 мм', price: 85 },
    { value: '75x75', label: '75x75 мм', price: 70 },
    { value: '100x100', label: '100x100 мм', price: 60 }
  ]

  const wireDiameters = [
    { value: '1.6', label: '1.6 мм', multiplier: 0.8 },
    { value: '2.0', label: '2.0 мм', multiplier: 1.0 },
    { value: '2.5', label: '2.5 мм', multiplier: 1.3 },
    { value: '3.0', label: '3.0 мм', multiplier: 1.6 }
  ]

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const calculateCost = () => {
    const { width, height, meshSize, wireDiameter, quantity } = formData
    
    if (!width || !height) {
      alert('Пожалуйста, введите размеры')
      return
    }

    const widthNum = parseFloat(width)
    const heightNum = parseFloat(height)
    const quantityNum = parseInt(quantity)

    if (widthNum <= 0 || heightNum <= 0 || quantityNum <= 0) {
      alert('Размеры и количество должны быть больше нуля')
      return
    }

    const selectedMesh = meshSizes.find(mesh => mesh.value === meshSize)
    const selectedWire = wireDiameters.find(wire => wire.value === wireDiameter)

    const area = widthNum * heightNum
    const basePrice = selectedMesh.price * selectedWire.multiplier
    const totalArea = area * quantityNum
    const totalCost = totalArea * basePrice

    setResult({
      area: area.toFixed(2),
      totalArea: totalArea.toFixed(2),
      pricePerSqm: basePrice.toFixed(2),
      totalCost: totalCost.toFixed(2),
      meshSize: selectedMesh.label,
      wireDiameter: selectedWire.label
    })
  }

  const resetForm = () => {
    setFormData({
      width: '',
      height: '',
      meshSize: '50x50',
      wireDiameter: '2.0',
      quantity: 1
    })
    setResult(null)
  }

  return (
    <div className="calculator-page">
      <div className="container">
        <div className="calculator-header">
          <CalcIcon size={48} className="calculator-icon" />
          <h1>Калькулятор стоимости сетки рабицы</h1>
          <p>Рассчитайте необходимое количество и стоимость сетки для вашего проекта</p>
        </div>

        <div className="calculator-content">
          <div className="calculator-form">
            <div className="card">
              <h2>Параметры расчета</h2>
              
              <div className="form-group">
                <label htmlFor="width">Ширина (м)</label>
                <input
                  type="number"
                  id="width"
                  name="width"
                  value={formData.width}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="Например: 10"
                  step="0.1"
                  min="0"
                />
              </div>

              <div className="form-group">
                <label htmlFor="height">Высота (м)</label>
                <input
                  type="number"
                  id="height"
                  name="height"
                  value={formData.height}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="Например: 2"
                  step="0.1"
                  min="0"
                />
              </div>

              <div className="form-group">
                <label htmlFor="meshSize">Размер ячейки</label>
                <select
                  id="meshSize"
                  name="meshSize"
                  value={formData.meshSize}
                  onChange={handleInputChange}
                  className="input"
                >
                  {meshSizes.map(mesh => (
                    <option key={mesh.value} value={mesh.value}>
                      {mesh.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="wireDiameter">Диаметр проволоки</label>
                <select
                  id="wireDiameter"
                  name="wireDiameter"
                  value={formData.wireDiameter}
                  onChange={handleInputChange}
                  className="input"
                >
                  {wireDiameters.map(wire => (
                    <option key={wire.value} value={wire.value}>
                      {wire.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="quantity">Количество рулонов</label>
                <input
                  type="number"
                  id="quantity"
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleInputChange}
                  className="input"
                  min="1"
                />
              </div>

              <div className="form-actions">
                <button onClick={calculateCost} className="btn btn-primary">
                  Рассчитать
                </button>
                <button onClick={resetForm} className="btn btn-secondary">
                  Сбросить
                </button>
              </div>
            </div>
          </div>

          <div className="calculator-result">
            {result ? (
              <div className="card result-card">
                <h2>Результат расчета</h2>
                
                <div className="result-item">
                  <span>Площадь одного рулона:</span>
                  <strong>{result.area} м²</strong>
                </div>
                
                <div className="result-item">
                  <span>Общая площадь:</span>
                  <strong>{result.totalArea} м²</strong>
                </div>
                
                <div className="result-item">
                  <span>Размер ячейки:</span>
                  <strong>{result.meshSize}</strong>
                </div>
                
                <div className="result-item">
                  <span>Диаметр проволоки:</span>
                  <strong>{result.wireDiameter}</strong>
                </div>
                
                <div className="result-item">
                  <span>Цена за м²:</span>
                  <strong>{result.pricePerSqm} ₽</strong>
                </div>
                
                <div className="result-item total">
                  <span>Общая стоимость:</span>
                  <strong>{result.totalCost} ₽</strong>
                </div>

                <div className="result-actions">
                  <button className="btn btn-primary">
                    <Package size={20} />
                    Заказать
                  </button>
                  <a href="tel:+78001234567" className="btn btn-secondary">
                    Позвонить для уточнения
                  </a>
                </div>
              </div>
            ) : (
              <div className="card info-card">
                <Info size={48} className="info-icon" />
                <h3>Как пользоваться калькулятором</h3>
                <ul>
                  <li>Введите размеры участка (ширина и высота)</li>
                  <li>Выберите размер ячейки сетки</li>
                  <li>Выберите диаметр проволоки</li>
                  <li>Укажите количество рулонов</li>
                  <li>Нажмите "Рассчитать" для получения результата</li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Calculator