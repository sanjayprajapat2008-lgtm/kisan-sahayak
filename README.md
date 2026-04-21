# किसान सहायक — Kisan Sahayak

A Hindi voice assistant for farmers, built with Python and Flask.

## Features

- 🌾 **Hindi Voice Input/Output** — Speak and listen in Hindi
- 🌤️ **Weather Information** — Current weather and rain forecasts
- 💰 **Mandi Prices** — Real-time crop prices
- 🌱 **Farming Advice** — Crop info, soil types, fertilizers, irrigation
- 🐛 **Pest Control** — Tips for pest management
- 🏛️ **Government Schemes** — Info on PM Kisan, crop insurance, etc.
- 💻 **Web Interface** — Chat-based UI with voice buttons

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Weather API Key (Free)

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. The API key is already configured in `weather.py` ✅

### 3. Run the App

```bash
python main.py
```

Then open http://localhost:5000 in your browser.

## Usage

- **Web**: Type questions in Hindi or use voice input
- **Voice**: The app listens continuously in the background
- **Supported Topics**: Weather, rain, mandi prices, crops, soil, fertilizers, irrigation, pests, govt schemes

## API Usage

To use the API programmatically, ensure UTF-8 encoding for Hindi text:

```python
import requests

response = requests.post("http://localhost:5000/ask", 
    json={"question": "नमस्ते", "city": "Jodhpur"},
    headers={"Content-Type": "application/json; charset=utf-8"}
)
```

## Files

- `main.py` — Flask web server
- `brain.py` — AI logic for answering questions
- `weather.py` — Weather API integration
- `speech.py` — Voice recognition and TTS
- `templates/index.html` — Web interface

## Requirements

- Python 3.8+
- Microphone (for voice input)
- Internet connection (for weather API and TTS)
- Speakers/headphones (for voice output)

## Troubleshooting

- **No microphone**: Install PyAudio: `pip install pyaudio`
- **Weather not working**: Check your OpenWeatherMap API key
- **Voice not working**: Check internet and microphone permissions