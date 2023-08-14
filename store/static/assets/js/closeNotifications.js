(function() {
    document.querySelectorAll('.notification-card .close').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            card = el.closest('.notification-card')
            card.classList.add('hidden');
            setTimeout(() => {
                card.remove();
            }, 600);
        });
    });
})();
