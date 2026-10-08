// background.js
console.log('ImpersonAI: Background service worker started.');

// Example: You can listen for tab updates here if needed
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // You could trigger a check from here if you want to warn on page load
        // but the content script handles click-based interception.
        console.log('ImpersonAI: Tab updated:', tab.url);
    }
});