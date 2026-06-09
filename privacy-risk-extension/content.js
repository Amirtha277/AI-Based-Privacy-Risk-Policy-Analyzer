// 🔥 Smart Policy Detection

const urlKeywords = [
    "privacy",
    "policy",
    "terms",
    "conditions",
    "legal",
    "gdpr"
];

const titleKeywords = [
    "privacy policy",
    "terms of service",
    "terms and conditions",
    "user agreement",
    "data policy"
];

const textKeywords = [
    "personal data",
    "information we collect",
    "how we use your information",
    "third party",
    "data sharing",
    "cookies",
    "data retention"
];

function detectPolicyPage() {

    const url = window.location.href.toLowerCase();
    const title = document.title.toLowerCase();
    const bodyText = document.body.innerText.toLowerCase();

    let score = 0;

    // URL check
    urlKeywords.forEach(k => {
        if (url.includes(k)) score += 2;
    });

    // Title check
    titleKeywords.forEach(k => {
        if (title.includes(k)) score += 2;
    });

    // Text keyword count
    let keywordMatches = 0;

    textKeywords.forEach(k => {
        if (bodyText.includes(k)) keywordMatches++;
    });

    if (keywordMatches >= 3) score += 2;

    // Policy pages are usually long
    if (bodyText.length > 3000) score += 1;

    return score >= 3;
}

// Wait until page fully loads
window.addEventListener("load", function () {
    if (detectPolicyPage()) {
        showAnalyzeButton();
    }
});




// 🔘 Floating Button
function showAnalyzeButton() {

    // Prevent duplicate button
    if (document.getElementById("privacyRiskBtn")) return;

    const button = document.createElement("button");
    button.id = "privacyRiskBtn";
    button.innerText = "🔍 Analyze Policy";

    button.style.position = "fixed";
    button.style.bottom = "20px";
    button.style.right = "20px";
    button.style.zIndex = "9999";
    button.style.padding = "12px 16px";
    button.style.background = "#4CAF50";
    button.style.color = "white";
    button.style.border = "none";
    button.style.borderRadius = "8px";
    button.style.cursor = "pointer";
    button.style.fontSize = "14px";
    button.style.boxShadow = "0 4px 10px rgba(0,0,0,0.3)";

    document.body.appendChild(button);

    button.addEventListener("click", function () {
        analyzePage();
    });
}


// 📡 Call Flask API
function analyzePage() {

    fetch("http://127.0.0.1:5000/analyze_api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: window.location.href,
            lang: "en"
        })
    })
    .then(response => response.json())
    .then(data => {
        showResultOverlay(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


// 📊 Show Result Overlay
function showResultOverlay(data) {

    const overlay = document.createElement("div");
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.background = "rgba(0,0,0,0.7)";
    overlay.style.zIndex = "10000";
    overlay.style.display = "flex";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";

    const box = document.createElement("div");
    box.style.background = "white";
    box.style.padding = "20px";
    box.style.width = "420px";
    box.style.borderRadius = "12px";
    box.style.textAlign = "center";

    const title = document.createElement("h2");
    title.textContent = "Privacy Risk Score: " + (data.score || 0) + "/100";

    const img = document.createElement("img");
    img.src = "data:image/png;base64," + (data.image_base64 || "");
    img.style.width = "100%";
    img.style.marginTop = "10px";

    const audioTitle = document.createElement("h4");
    audioTitle.textContent = "Audio Explanation";

    const audio = document.createElement("audio");
    audio.controls = true;
    audio.style.width = "100%";

    const source = document.createElement("source");
    source.src = "data:audio/mpeg;base64," + (data.audio_base64 || "");
    source.type = "audio/mpeg";

    audio.appendChild(source);

    const closeBtn = document.createElement("button");
    closeBtn.textContent = "Close";
    closeBtn.style.marginTop = "15px";
    closeBtn.style.padding = "8px 14px";
    closeBtn.style.border = "none";
    closeBtn.style.background = "#f44336";
    closeBtn.style.color = "white";
    closeBtn.style.borderRadius = "6px";
    closeBtn.style.cursor = "pointer";

    closeBtn.onclick = () => overlay.remove();

    box.appendChild(title);
    box.appendChild(img);
    box.appendChild(audioTitle);
    box.appendChild(audio);
    box.appendChild(closeBtn);

    overlay.appendChild(box);
    document.body.appendChild(overlay);
    };
