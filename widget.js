document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('local-info');
    if (!container) return;

    try {
        // Fetch IP and Location
        const geoResponse = await fetch('https://get.geojs.io/v1/ip/geo.json');
        if (!geoResponse.ok) throw new Error('Failed to fetch geo data');
        const geoData = await geoResponse.json();

        const lat = geoData.latitude;
        const lon = geoData.longitude;
        const city = geoData.city;
        const timezone = geoData.timezone;

        // Fetch Weather from Open-Meteo
        const weatherResponse = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`);
        if (!weatherResponse.ok) throw new Error('Failed to fetch weather data');
        const weatherData = await weatherResponse.json();

        const temp = weatherData.current_weather.temperature;

        // Compute Local Time based on the user's IP timezone
        const timeOptions = {
            timeZone: timezone,
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        };
        const localTime = new Intl.DateTimeFormat([], timeOptions).format(new Date());

        container.innerHTML = `<span>📍 ${city}</span> | <span>🕒 ${localTime}</span> | <span>🌡️ ${temp}°C</span>`;

    } catch (error) {
        console.error('Error fetching local info:', error);
    }
});


// WebSDR Terminal Logic
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('websdr-btn');
    if (!btn) return;

    // Inject modal HTML
    const modalHtml = `
    <div id="terminal-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; justify-content: center; align-items: center;">
        <div style="width: 80%; max-width: 600px; height: 400px; background: #000; border: 2px solid #333; border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.5); font-family: monospace; color: #fff; padding: 20px; position: relative; overflow-y: auto;">
            <div style="position: absolute; top: 5px; right: 10px; cursor: pointer; font-size: 1.2rem; color: #aaa;" id="close-terminal">x</div>
            <div id="terminal-output">
                Root@bt:~# ssh websdr.0m364.com<br>
            </div>
            <div id="terminal-input-line" style="display: flex; margin-top: 5px;">
                <span id="terminal-prompt" style="margin-right: 10px;">bt login:</span>
                <input type="text" id="terminal-input" style="background: transparent; border: none; color: #fff; font-family: monospace; outline: none; flex-grow: 1; font-size: 1rem;">
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const modal = document.getElementById('terminal-modal');
    const closeBtn = document.getElementById('close-terminal');
    const input = document.getElementById('terminal-input');
    const output = document.getElementById('terminal-output');
    const prompt = document.getElementById('terminal-prompt');
    const inputLine = document.getElementById('terminal-input-line');

    let step = 'login';

    btn.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.display = 'flex';
        input.focus();
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        resetTerminal();
    });


    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    function resetTerminal() {
        step = 'login';
        output.innerHTML = 'Root@bt:~# ssh websdr.0m364.com<br>';
        prompt.innerText = 'bt login:';
        input.type = 'text';
        input.value = '';
        inputLine.style.display = 'flex';
    }

    input.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            const val = input.value;
            input.value = '';

            if (step === 'login') {
                output.innerHTML += `bt login: ${escapeHtml(val)}<br>`;
                if (val.trim() === 'root') {
                    step = 'password';
                    prompt.innerText = 'Password:';
                    input.type = 'password';
                } else {
                    output.innerHTML += `Login incorrect<br>`;
                    setTimeout(resetTerminal, 1000);
                }
            } else if (step === 'password') {
                output.innerHTML += `Password: ${'*'.repeat(val.length)}<br>`;

                try {
                    const encrypted = 'U2FsdGVkX1/hBV++BeqMbngTJUutPCH2DCHQQHernak=';
                    if (typeof CryptoJS !== 'undefined') {
                        const bytes = CryptoJS.AES.decrypt(encrypted, val);
                        const originalText = bytes.toString(CryptoJS.enc.Utf8);

                        if (originalText === 'ACCESS_GRANTED') {
                            inputLine.style.display = 'none';
                            output.innerHTML += `<span style="color: #0f0;">Access Granted. Decrypting signal intelligence...</span><br>`;

                            try {
                                const res = await fetch('https://api.counterapi.dev/v1/0m364/websdr_login_attempts/up');
                                const data = await res.json();
                                output.innerHTML += `<span style="color: #0f0;">Connection Established. Successful accesses: ${data.count}</span><br>`;
                            } catch (err) {
                                output.innerHTML += `<span style="color: #0f0;">Connection Established. Counter unavailable.</span><br>`;
                            }
                        } else {
                            output.innerHTML += `Login incorrect<br>`;
                            resetTerminal();
                        }
                    } else {
                        output.innerHTML += `<span style="color: #f00;">Error: Encryption library not loaded.</span><br>`;
                        resetTerminal();
                    }
                } catch (err) {
                    output.innerHTML += `Login incorrect<br>`;
                    setTimeout(resetTerminal, 1000);
                }
            }
        }
    });
});
