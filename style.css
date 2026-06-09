document.getElementById("analyzeBtn").addEventListener("click", async () => {

    const lang = document.getElementById("language").value;

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Analyzing...";

    try {

        const response = await fetch("http://127.0.0.1:5000/analyze_api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: tab.url,
                lang: lang
            })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = "Error: " + data.error;
            return;
        }

        let risksHTML = "";
        data.risks.forEach(risk => {
            risksHTML += `<li>${risk.clause} (${risk.level})</li>`;
        });

        resultDiv.innerHTML = `
            <h3>Score: ${data.score}/100</h3> 
            <ul>${risksHTML}</ul>
           <img src="data:image/png;base64,${data.image_base64}" width="100%">
            <h4 style="margin-top:10px;">Audio Explanation</h4>
    <audio controls style="width:100%;">
    <source src="data:audio/mpeg;base64,${data.audio_base64}" type="audio/mpeg">
</audio>
        `;

    } catch (error) {
        resultDiv.innerHTML = "Connection failed. Is Flask running?";
    }

});