# ============================================================
#  weather.py — Hindi Voice Assistant (Kisan Sahayak)
#  Get weather info and return answers in Hindi
#  Uses FREE OpenWeatherMap API (no credit card needed)
#  Author: Your Name | College Project
# ============================================================

import requests
import json
from datetime import datetime

# ─── Your FREE API Key ────────────────────────────────────────
# Step 1: Go to https://openweathermap.org/api
# Step 2: Click "Sign Up" — it is FREE, no credit card needed
# Step 3: After login, go to "My API Keys" tab
# Step 4: Copy your key and paste it below
API_KEY = "1d15296b3a0aaf3512034b9cf81d671b"   # <-- paste your key here

# ─── Settings ─────────────────────────────────────────────────
BASE_URL        = "https://api.openweathermap.org/data/2.5/"
DEFAULT_CITY    = "Jodhpur"          # change to your city
UNITS           = "metric"           # Celsius temperature
CACHE_MINUTES   = 10                 # avoid too many API calls
# ─────────────────────────────────────────────────────────────

# Simple cache to avoid hitting API too often
_cache = {}


# ─── Hindi translations for weather descriptions ──────────────
WEATHER_HINDI = {
    "clear sky":              "साफ आसमान",
    "few clouds":             "थोड़े बादल",
    "scattered clouds":       "छितरे बादल",
    "broken clouds":          "टूटे बादल",
    "overcast clouds":        "घने बादल",
    "light rain":             "हल्की बारिश",
    "moderate rain":          "मध्यम बारिश",
    "heavy intensity rain":   "तेज़ बारिश",
    "thunderstorm":           "आंधी तूफ़ान",
    "snow":                   "बर्फ़बारी",
    "mist":                   "धुंध",
    "fog":                    "कोहरा",
    "haze":                   "धुंआ",
    "dust":                   "धूल",
    "sand":                   "रेत की आंधी",
    "drizzle":                "बूंदाबांदी",
}

# Hindi names for days of week
DAYS_HINDI = {
    "Monday":    "सोमवार",
    "Tuesday":   "मंगलवार",
    "Wednesday": "बुधवार",
    "Thursday":  "गुरुवार",
    "Friday":    "शुक्रवार",
    "Saturday":  "शनिवार",
    "Sunday":    "रविवार",
}


def _translate_weather(english_desc):
    """Convert English weather description to Hindi."""
    desc = english_desc.lower()
    for eng, hindi in WEATHER_HINDI.items():
        if eng in desc:
            return hindi
    return english_desc  # return original if no translation found


def _is_cache_valid(key):
    """Check if cached data is still fresh."""
    if key not in _cache:
        return False
    age_seconds = (datetime.now() - _cache[key]["time"]).seconds
    return age_seconds < (CACHE_MINUTES * 60)


def _check_api_key():
    """Validate that the API key has been set."""
    if API_KEY == "YOUR_FREE_API_KEY_HERE" or API_KEY.strip() == "":
        print("[ERROR] API key not set!")
        print("[TIP]   1. Go to https://openweathermap.org/api")
        print("[TIP]   2. Sign up FREE and copy your API key")
        print("[TIP]   3. Paste it in weather.py where it says API_KEY = ...")
        return False
    return True


def mausam_batao(city=DEFAULT_CITY):
    """
    Get TODAY's current weather and return answer in Hindi.

    Example output:
    "जोधपुर में आज साफ आसमान है। तापमान 32 डिग्री है।
     हवा की गति 12 किलोमीटर प्रति घंटा है।
     नमी 45 प्रतिशत है।"
    """
    print(f"[DEBUG] Using API key: {API_KEY}")
    if not _check_api_key():
        return "माफ करें, मौसम की जानकारी अभी उपलब्ध नहीं है।"

    cache_key = f"current_{city}"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        url = BASE_URL + "weather"
        params = {
            "q":     city,
            "appid": API_KEY,
            "units": UNITS,
        }
        response = requests.get(url, params=params, timeout=5)

        # ── Handle HTTP errors ─────────────────────────────
        if response.status_code == 401:
            return "API key गलत है। कृपया weather.py में सही key डालें।"

        if response.status_code == 404:
            return f"शहर '{city}' नहीं मिला। कृपया सही शहर का नाम बताएं।"

        if response.status_code == 429:
            return "बहुत ज़्यादा requests हो गई। थोड़ी देर बाद पूछें।"

        response.raise_for_status()

        data = response.json()

        # ── Extract weather info ───────────────────────────
        city_name   = data["name"]
        temp        = round(data["main"]["temp"])
        feels_like  = round(data["main"]["feels_like"])
        humidity    = data["main"]["humidity"]
        wind_speed  = round(data["wind"]["speed"] * 3.6)  # m/s to km/h
        desc_eng    = data["weather"][0]["description"]
        desc_hindi  = _translate_weather(desc_eng)

        # ── Build Hindi reply ──────────────────────────────
        reply = (
            f"{city_name} में आज {desc_hindi} है। "
            f"तापमान {temp} डिग्री सेल्सियस है। "
            f"महसूस होता है {feels_like} डिग्री जैसा। "
            f"हवा की गति {wind_speed} किलोमीटर प्रति घंटा है। "
            f"नमी {humidity} प्रतिशत है।"
        )

        # Add farming tip based on weather
        reply += _kisan_tip_mausam(temp, desc_eng, humidity, wind_speed)

        # Cache result
        _cache[cache_key] = {"data": reply, "time": datetime.now()}
        return reply

    except requests.exceptions.ConnectionError:
        return "इंटरनेट कनेक्शन नहीं है। कृपया इंटरनेट चेक करें।"

    except requests.exceptions.Timeout:
        return "सर्वर का जवाब देर से आ रहा है। थोड़ी देर बाद फिर पूछें।"

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Weather API error: {e}")
        return "मौसम की जानकारी नहीं मिल पाई। बाद में कोशिश करें।"

    except (KeyError, ValueError) as e:
        print(f"[ERROR] Unexpected API response format: {e}")
        return "मौसम डेटा पढ़ने में समस्या हुई।"


def barish_hogi(city=DEFAULT_CITY):
    """
    Get 5-day weather forecast and check for rain.
    Returns Hindi answer about upcoming rain.

    Example output:
    "जोधपुर में अगले 3 दिनों में बारिश की संभावना है।
     कल बुधवार को हल्की बारिश होगी।"
    """

    if not _check_api_key():
        return "माफ करें, बारिश की जानकारी अभी उपलब्ध नहीं है।"

    cache_key = f"forecast_{city}"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        url = BASE_URL + "forecast"
        params = {
            "q":     city,
            "appid": API_KEY,
            "units": UNITS,
            "cnt":   40,  # 5 days × 8 readings per day
        }
        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 401:
            return "API key गलत है।"
        if response.status_code == 404:
            return f"शहर '{city}' नहीं मिला।"

        response.raise_for_status()
        data = response.json()

        # ── Find rain days in forecast ─────────────────────
        rain_days = []
        seen_dates = set()

        for item in data["list"]:
            dt       = datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime("%Y-%m-%d")
            day_name = DAYS_HINDI.get(dt.strftime("%A"), dt.strftime("%A"))
            desc     = item["weather"][0]["description"].lower()

            if date_str not in seen_dates and date_str != datetime.now().strftime("%Y-%m-%d"):
                seen_dates.add(date_str)
                if "rain" in desc or "drizzle" in desc or "storm" in desc:
                    rain_days.append({
                        "day":  day_name,
                        "desc": _translate_weather(item["weather"][0]["description"]),
                        "temp": round(item["main"]["temp"])
                    })

        # ── Build Hindi reply ──────────────────────────────
        city_name = data["city"]["name"]

        if not rain_days:
            reply = (
                f"{city_name} में अगले 5 दिनों में बारिश की संभावना नहीं है। "
                f"आसमान साफ रहेगा। खेती के काम जारी रख सकते हैं।"
            )
        elif len(rain_days) == 1:
            r = rain_days[0]
            reply = (
                f"{city_name} में {r['day']} को {r['desc']} होगी। "
                f"तापमान {r['temp']} डिग्री रहेगा। "
                f"उस दिन खेत में काम कम करें।"
            )
        else:
            days_str = ", ".join([r["day"] for r in rain_days])
            reply = (
                f"{city_name} में अगले कुछ दिनों में बारिश की संभावना है। "
                f"{days_str} को बारिश हो सकती है। "
                f"फसल को सुरक्षित रखें और सिंचाई कम करें।"
            )

        _cache[cache_key] = {"data": reply, "time": datetime.now()}
        return reply

    except requests.exceptions.ConnectionError:
        return "इंटरनेट कनेक्शन नहीं है।"

    except requests.exceptions.Timeout:
        return "सर्वर का जवाब नहीं आया। बाद में कोशिश करें।"

    except Exception as e:
        print(f"[ERROR] Forecast error: {e}")
        return "बारिश की जानकारी नहीं मिल पाई।"


def _kisan_tip_mausam(temp, desc_eng, humidity, wind_speed):
    """
    Return a short Hindi farming tip based on current weather.
    Called automatically by mausam_batao().
    """
    tip = ""
    desc = desc_eng.lower()

    if temp > 40:
        tip = " बहुत गर्मी है — फसलों को ज़्यादा पानी दें।"
    elif temp < 10:
        tip = " ठंड ज़्यादा है — फसलों को पाले से बचाएं।"
    elif "rain" in desc or "drizzle" in desc:
        tip = " बारिश है — आज सिंचाई की ज़रूरत नहीं।"
    elif "storm" in desc:
        tip = " आंधी आ सकती है — फसल और उपकरण सुरक्षित करें।"
    elif humidity > 80:
        tip = " नमी ज़्यादा है — फसल में फफूंद से सावधान रहें।"
    elif wind_speed > 30:
        tip = " तेज़ हवा है — खड़ी फसलों का ध्यान रखें।"

    return tip


# ─── Run directly to test ─────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KISAN SAHAYAK — WEATHER MODULE TEST")
    print("=" * 55)

    test_city = "Jodhpur"

    print(f"\n[TEST 1] Current weather for {test_city}...")
    result1 = mausam_batao(test_city)
    print(f"HINDI REPLY: {result1}")

    print(f"\n[TEST 2] Rain forecast for {test_city}...")
    result2 = barish_hogi(test_city)
    print(f"HINDI REPLY: {result2}")

    print("\n[DONE] Weather module test complete!")
    print("[TIP]  If you see API errors, set your API_KEY in this file.")
