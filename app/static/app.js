// Подключаем Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand();

// Функция переключения экранов
function switchScreen(screenId, btn) {
// 1. Скрываем все экраны
document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));

// 2. Убираем активный класс со всех кнопок меню
document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));

// 3. Показываем нужный экран и подсвечиваем кнопку
const targetScreen = document.getElementById('screen-' + screenId);
if (targetScreen) {
targetScreen.classList.add('active');
}
if (btn) {
btn.classList.add('active');
}
}

// Загружаем баланс (пока просто 100 для теста)
document.addEventListener('DOMContentLoaded', () => {
const balanceEls = document.querySelectorAll('#balance-val, #welcome-bal');
balanceEls.forEach(el => {
if (el) el.innerText = '100';
});
});
