const $ = (selector) => document.querySelector(selector)

const form = $('#carForm')
const fields = {
  maker: $('#makerInput'), model: $('#modelInput'), year: $('#yearInput'),
  mileage: $('#mileageInput'), price: $('#priceInput'), fuel: $('#fuelInput'),
  status: $('#statusInput'),
}
const submitButton = $('#submitButton')
const cancelButton = $('#cancelEditButton')
const searchInput = $('#searchInput')
const statusFilter = $('#statusFilter')
const carList = $('#carList')
const emptyMessage = $('#emptyMessage')
const countText = $('#countText')

let cars = [
  { id: 1, maker: '현대', model: '쏘나타', year: 2021, mileage: 43000, price: 1850, fuel: 'LPG', status: '판매중' },
  { id: 2, maker: '기아', model: 'K5', year: 2020, mileage: 52000, price: 1690, fuel: '가솔린', status: '예약중' },
]
let editingId = null

function filteredCars() {
  const keyword = searchInput.value.trim().toLowerCase()
  return cars.filter((car) =>
    `${car.maker} ${car.model}`.toLowerCase().includes(keyword) &&
    (statusFilter.value === '전체' || car.status === statusFilter.value)
  )
}

function renderCars() {
  const shown = filteredCars()
  countText.textContent = `전체 ${cars.length}대 / 표시 ${shown.length}대`
  emptyMessage.hidden = shown.length > 0
  carList.replaceChildren(...shown.map(createCarCard))
}

function createCarCard(car) {
  const card = document.createElement('article')
  card.className = 'car-card'
  card.innerHTML = `
    <h3></h3>
    <p class="info"></p>
    <p class="price"></p>
    <span class="status ${statusClass(car.status)}"></span>
    <div class="card-actions">
      <button type="button" class="edit-button" data-action="edit">수정</button>
      <button type="button" class="delete-button" data-action="delete">삭제</button>
    </div>`
  card.querySelector('h3').textContent = `${car.maker} ${car.model}`
  card.querySelector('.info').textContent = `${car.year}년식 · ${car.fuel} · ${car.mileage.toLocaleString()}km`
  card.querySelector('.price').textContent = `${car.price.toLocaleString()}만원`
  card.querySelector('.status').textContent = car.status
  card.querySelectorAll('button').forEach((button) => { button.dataset.id = car.id })
  return card
}

function statusClass(status) {
  return status === '판매중' ? 'selling' : status === '예약중' ? 'reserved' : 'sold'
}

function readForm() {
  const car = Object.fromEntries(Object.entries(fields).map(([key, field]) => [key, field.value.trim()]))
  const maxYear = new Date().getFullYear()
  const checks = [
    [!car.maker, '제조사를 선택하세요.', fields.maker],
    [!car.model, '모델명을 입력하세요.', fields.model],
    [!car.year || +car.year < 1990 || +car.year > maxYear, `연식은 1990년부터 ${maxYear}년 사이로 입력하세요.`, fields.year],
    [!car.mileage || +car.mileage < 0, '주행거리는 0 이상으로 입력하세요.', fields.mileage],
    [!car.price || +car.price < 1, '가격은 1 이상 입력하세요.', fields.price],
    [!car.fuel, '연료를 선택하세요.', fields.fuel],
  ]
  const failed = checks.find(([invalid]) => invalid)
  if (failed) {
    alert(failed[1])
    failed[2].focus()
    return null
  }
  return { ...car, year: +car.year, mileage: +car.mileage, price: +car.price }
}

function resetForm() {
  editingId = null
  form.reset()
  submitButton.textContent = '등록'
  cancelButton.hidden = true
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  const car = readForm()
  if (!car) return

  if (editingId === null) cars.push({ ...car, id: Date.now() })
  else cars = cars.map((item) => item.id === editingId ? { ...car, id: editingId } : item)

  resetForm()
  renderCars()
})

carList.addEventListener('click', (event) => {
  const button = event.target.closest('button')
  if (!button) return
  const id = Number(button.dataset.id)

  if (button.dataset.action === 'delete') {
    if (!confirm('선택한 차량을 삭제할까요?')) return
    cars = cars.filter((car) => car.id !== id)
    if (editingId === id) resetForm()
  } else {
    const car = cars.find((item) => item.id === id)
    Object.entries(fields).forEach(([key, field]) => { field.value = car[key] })
    editingId = id
    submitButton.textContent = '수정 완료'
    cancelButton.hidden = false
    fields.model.focus()
  }
  renderCars()
})

cancelButton.addEventListener('click', resetForm)
searchInput.addEventListener('input', renderCars)
statusFilter.addEventListener('change', renderCars)
renderCars()
