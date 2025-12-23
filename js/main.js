document.addEventListener('DOMContentLoaded', () => {
    // Установка текущей даты
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = today.toLocaleDateString('ru-RU', options);
    }

    // Обработка всех кнопок "Читать далее" в статьях
    document.querySelectorAll('article').forEach(article => {
        const btn = article.querySelector('.read-more-btn');
        if (!btn) return;

        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const content = document.getElementById(targetId);
            const isExpanded = btn.classList.contains('expanded');

            // Переключаем состояние
            btn.classList.toggle('expanded');
            btn.setAttribute('aria-expanded', !isExpanded);
            content.hidden = isExpanded;
        });
    });

    // Обработка клика по ссылке в кратких новостях (предотвращает конфликты)
    document.querySelectorAll('.brief-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const article = link.closest('.brief-item');
            const btn = article.querySelector('.read-more-btn');
            if (btn && !link.href.includes('#')) {
                e.preventDefault();
                btn.click();
            }
        });
    });
});