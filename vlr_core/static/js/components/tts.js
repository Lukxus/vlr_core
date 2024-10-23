document.getElementById('speakBtn').addEventListener('click', function() {
    const synth = window.speechSynthesis;
    const texts = [
        document.getElementById('text-1'),
        document.getElementById('text-2'),
        document.getElementById('text-3'),
        document.getElementById('text-4'),
        document.getElementById('text-5'),
        document.getElementById('text-6')
    ];

    function removeHighlight() {
        texts.forEach(text => {
            text.classList.remove('highlight');
        });
    }

    let index = 0;
    function speakText() {
        if (index < texts.length) {
            const textElement = texts[index];
            const utterThis = new SpeechSynthesisUtterance(textElement.innerText);
            utterThis.lang = 'pt-BR';
            removeHighlight();
            textElement.classList.add('highlight');

            utterThis.onend = function() {
                index++;
                speakText();
            };

            synth.speak(utterThis);
        } else {
            removeHighlight();
        }
    }

    speakText();
});
