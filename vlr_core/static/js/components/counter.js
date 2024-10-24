function animateCounter(id, start, end, duration, subtextId, isPercentage = false) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const currentValue = Math.floor(progress * (end - start) + start);
        obj.innerText = isPercentage ? `${currentValue}%` : currentValue.toLocaleString('pt-BR');
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            document.getElementById(subtextId).style.display = 'block';
        }
    };
    window.requestAnimationFrame(step);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('[data-counter]').forEach(counterElement => {
        const id = counterElement.getAttribute('id');
        const endValue = parseInt(counterElement.getAttribute('data-end-value'), 10);
        const duration = parseInt(counterElement.getAttribute('data-duration'), 10);
        const subtextId = counterElement.getAttribute('data-subtext-id');
        const isPercentage = counterElement.getAttribute('data-is-percentage') === 'true';

        animateCounter(id, 0, endValue, duration, subtextId, isPercentage);
    });
});
