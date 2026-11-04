const tg = window.Telegram.WebApp;
tg.expand();

// Загружаем баланс с сервера
async function loadBalance() {
    try {
        const response = await fetch('/api/balance', {
            headers: { 'Authorization': tg.initData }
        });
        if (response.ok) {
            const data = await response.json();
            
            // Обновляем все цифры баланса на экране
            document.querySelectorAll('.balance strong, .welcome-balance strong, .profile-balance strong, .game-score strong').forEach(el => {
                el.innerText = data.balance;
            });

            // Меняем имя пользователя
            if (tg.initDataUnsafe.user) {
                document.querySelector('.user-info strong').innerText = tg.initDataUnsafe.user.first_name;
                document.querySelector('.profile-card h2').innerText = tg.initDataUnsafe.user.first_name;
            }
        }
    } catch (e) {
        console.error("Ошибка загрузки баланса:", e);
    }
}

// Кнопка "Пополнить"
document.querySelector('.add-balance').addEventListener('click', () => {
    tg.showAlert("💳 Пополнение скоро появится!");
});

// Кнопка "Играть" (переход в игру)
document.querySelector('.play-button').addEventListener('click', () => {
    document.getElementById('game-open').checked = true;
});

// Запускаем при старте
document.addEventListener('DOMContentLoaded', loadBalance);
// Скрипт для экрана загрузки
document.addEventListener('DOMContentLoaded', () => {
    // Через 2 секунды скрываем загрузку
    setTimeout(() => {
        const splash = document.getElementById('splash');
        if (splash) {
            splash.classList.add('hide');
            // Полностью удаляем из DOM через 0.5 сек (когда анимация закончится)
            setTimeout(() => splash.remove(), 500);
        }
    }, 2000);
});
