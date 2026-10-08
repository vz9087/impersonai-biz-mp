// content.js

// Function to check a URL with your FastAPI backend
async function checkUrl(url) {
    try {
        const response = await fetch('http://127.0.0.1:8000/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        return await response.json();
    } catch (error) {
        console.error('ImpersonAI: Failed to reach backend', error);
        return null;
    }
}

// Function to intercept link clicks
document.addEventListener('click', async (event) => {
    const link = event.target.closest('a');
    if (!link || !link.href) return;

    // Prevent the browser from following the link immediately
    event.preventDefault();
    event.stopPropagation();

    // Show a "checking" indicator (optional)
    console.log('ImpersonAI: Checking URL...', link.href);

    const result = await checkUrl(link.href);

    if (result && result.risk_level === 'HIGH') {
        // Show a warning overlay
        showWarningOverlay(link.href, result.probability);
    } else {
        // Safe or backend unavailable: navigate normally
        window.location.href = link.href;
    }
}, true); // Use capture phase to catch the click before other handlers[citation:3]

// Warning overlay function
function showWarningOverlay(url, probability) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.85); color: white; z-index: 999999;
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; font-family: sans-serif; text-align: center;
  `;

    overlay.innerHTML = `
    <h1 style="font-size: 3em; color: #ff4444;">⚠️ Dangerous Link Detected</h1>
    <p style="font-size: 1.2em; margin: 20px 0;">ImpersonAI has blocked this link:</p>
    <p style="font-size: 1em; color: #aaa; word-break: break-all;">${url}</p>
    <p style="font-size: 1.5em; color: #ffaa00;">Risk Score: ${(probability * 100).toFixed(1)}%</p>
    <button id="proceed-btn" style="margin-top: 30px; padding: 15px 30px; font-size: 1.2em; background: #444; color: white; border: 1px solid #666; border-radius: 8px; cursor: pointer;">
      I understand the risk, proceed anyway
    </button>
  `;

    document.body.appendChild(overlay);

    document.getElementById('proceed-btn').onclick = () => {
        window.location.href = url;
    };
}