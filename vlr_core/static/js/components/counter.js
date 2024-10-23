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
    animateCounter('counter1', 0, 30858, 1500, 'subtext1');
    animateCounter('counter2', 0, 45354, 1500, 'subtext2');
    animateCounter('counter3', 0, 8712, 1500, 'subtext3');
    animateCounter('counter4', 0, 66, 1500, 'subtext4', true);
});
