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
