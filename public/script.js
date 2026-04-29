document.getElementById('calculateBtn').addEventListener('click', async () => {
    const distance = parseFloat(document.getElementById('distance').value);
    const speed = parseFloat(document.getElementById('speed').value);
    const terrainType = document.getElementById('terrainType').value;
    const trafficScore = parseInt(document.getElementById('trafficScore').value);

    const resultArea = document.getElementById('resultArea');
    const errorArea = document.getElementById('errorArea');

    try {
        const response = await fetch('/api/delivery/estimate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ distance, speed, terrainType, trafficScore })
        });

        const data = await response.json();

        if (response.ok) {
            resultArea.classList.remove('hidden');
            errorArea.classList.add('hidden');
            document.getElementById('resultText').innerText = `Время в пути: ${data.time} ${data.unit}`;
        } else {
            throw new Error(data.message);
        }
    } catch (err) {
        errorArea.classList.remove('hidden');
        resultArea.classList.add('hidden');
        document.getElementById('errorText').innerText = err.message;
    }
});