// popup.js
document.getElementById('check-btn').onclick = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab.url) return;

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = 'Checking...';

    try {
        const response = await fetch('http://127.0.0.1:8000/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url })
        });
        const data = await response.json();

        resultDiv.className = data.risk_level === 'HIGH' ? 'high' : 'low';
        resultDiv.innerHTML = `<strong>${data.risk_level} RISK</strong><br>Probability: ${(data.probability * 100).toFixed(1)}%`;
    } catch (error) {
        resultDiv.textContent = 'Error: Backend not reachable.';
    }
};