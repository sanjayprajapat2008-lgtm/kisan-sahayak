# ============================================================
#  brain.py — Hindi Voice Assistant (Kisan Sahayak)
#  Understands farmer's Hindi questions and gives answers
#  Covers: Weather, Rain, Crops, Soil, Mandi Prices,
#          Fertilizer, Irrigation, Pest Control, Govt Schemes,
#          General Greetings
#  Author: Your Name | College Project
# ============================================================

# Weather functions imported dynamically to avoid caching issues

# ─── Mandi Prices (static data — update weekly) ───────────────
# In real project: fetch from https://agmarknet.gov.in API
MANDI_PRICES = {
    "गेहूं":      {"price": 2275, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "चावल":      {"price": 2183, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "बाजरा":     {"price": 2350, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "मक्का":     {"price": 1962, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "सरसों":     {"price": 5650, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "मूंगफली":   {"price": 6000, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "चना":       {"price": 5440, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "मूंग":      {"price": 7755, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "उड़द":      {"price": 6950, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "कपास":      {"price": 6620, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "प्याज":     {"price": 1200, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "आलू":       {"price": 1100, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "लहसुन":     {"price": 8000, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
    "जीरा":      {"price": 32000, "unit": "प्रति क्विंटल", "city": "जोधपुर मंडी"},
}

# ─── Crop Sowing Season Info ──────────────────────────────────
FASAL_JANKARI = {
    "गेहूं":    "गेहूं रबी फसल है। अक्टूबर से नवंबर में बोएं। अप्रैल में काटें।",
    "चावल":    "चावल खरीफ फसल है। जून से जुलाई में रोपाई करें। अक्टूबर में काटें।",
    "बाजरा":   "बाजरा खरीफ फसल है। जून में बोएं। सितंबर-अक्टूबर में काटें।",
    "मक्का":   "मक्का जून में बोएं। 90 दिन में तैयार होती है। पानी कम लगता है।",
    "सरसों":   "सरसों रबी फसल है। अक्टूबर में बोएं। मार्च में काटें।",
    "चना":     "चना अक्टूबर-नवंबर में बोएं। मार्च-अप्रैल में काटें। कम पानी चाहिए।",
    "मूंग":    "मूंग गर्मियों में मार्च-अप्रैल में बोएं। 60-65 दिन में तैयार।",
    "कपास":    "कपास अप्रैल-मई में बोएं। 6 से 8 महीने की फसल है।",
    "जीरा":    "जीरा अक्टूबर-नवंबर में बोएं। फरवरी-मार्च में काटें। राजस्थान में बहुत होता है।",
}

# ─── Soil Type Tips ───────────────────────────────────────────
MITTI_JANKARI = {
    "काली मिट्टी":   "काली मिट्टी कपास, गेहूं और सोयाबीन के लिए उत्तम है। पानी अच्छे से रोकती है।",
    "लाल मिट्टी":    "लाल मिट्टी मूंगफली, दालें और मोटे अनाज के लिए अच्छी है।",
    "रेतीली मिट्टी": "रेतीली मिट्टी में जीरा, बाजरा और मूंगफली अच्छे से होती है। ज़्यादा पानी दें।",
    "दोमट मिट्टी":   "दोमट मिट्टी सबसे अच्छी होती है। इसमें हर फसल होती है।",
    "चिकनी मिट्टी":  "चिकनी मिट्टी में धान और गेहूं उगाएं। जल निकासी का ध्यान रखें।",
}

# ─── Fertilizer Advice ────────────────────────────────────────
KHAD_JANKARI = {
    "यूरिया":    "यूरिया नाइट्रोजन खाद है। गेहूं और धान में बुआई के 3-4 हफ्ते बाद दें।",
    "डीएपी":     "डीएपी यानी DAP फास्फोरस खाद है। बुआई के समय खेत में मिलाएं।",
    "पोटाश":     "पोटाश खाद जड़ मज़बूत करती है। फल और सब्ज़ी की फसल में ज़रूर दें।",
    "जैविक खाद": "गोबर की खाद सबसे अच्छी है। बुआई से 1 महीने पहले खेत में मिलाएं।",
    "नीम खाद":   "नीम की खली खाद भी देती है और कीट भी भगाती है। बहुत फायदेमंद है।",
}

# ─── Irrigation Tips ──────────────────────────────────────────
SINCHAI_JANKARI = [
    "ड्रिप सिंचाई से 50 प्रतिशत पानी बचता है। सरकार से सब्सिडी मिलती है।",
    "फसल की जड़ों के पास पानी दें, पत्तियों पर नहीं।",
    "सुबह या शाम को सिंचाई करें। दोपहर में पानी बर्बाद होता है।",
    "गेहूं को 4 से 5 बार, सरसों को 2 से 3 बार पानी चाहिए।",
    "बाजरे में कम पानी लगता है — 2 से 3 सिंचाई काफी है।",
]

# ─── Pest Control Tips ────────────────────────────────────────
KEET_JANKARI = [
    "नीम का तेल पानी में मिलाकर स्प्रे करें — कीट भागते हैं।",
    "पीले चिपचिपे कार्ड खेत में लगाएं — उड़ने वाले कीट फंसते हैं।",
    "फसल चक्र अपनाएं — हर साल अलग फसल लगाने से कीट कम होते हैं।",
    "कीटनाशक दोपहर में न डालें — शाम को डालें, ज़्यादा असर होगा।",
    "जैविक कीटनाशक के लिए कृषि विभाग से संपर्क करें।",
]

# ─── Government Schemes ───────────────────────────────────────
YOJANA_JANKARI = {
    "पीएम किसान":        "पीएम किसान योजना में हर साल 6000 रुपये मिलते हैं। pmkisan.gov.in पर रजिस्टर करें।",
    "फसल बीमा":          "प्रधानमंत्री फसल बीमा योजना में फसल खराब होने पर मुआवज़ा मिलता है। बैंक से संपर्क करें।",
    "किसान क्रेडिट कार्ड": "किसान क्रेडिट कार्ड से कम ब्याज पर 3 लाख तक का लोन मिलता है।",
    "ड्रिप सब्सिडी":     "ड्रिप सिंचाई पर 50 से 90 प्रतिशत सब्सिडी मिलती है। कृषि विभाग में जाएं।",
    "सोलर पंप":          "पीएम कुसुम योजना में सोलर पंप पर 90 प्रतिशत सब्सिडी है।",
}

# ─── General Greetings ────────────────────────────────────────
GREETINGS = [
    "नमस्ते", "हेलो", "हाय", "प्रणाम", "राम राम",
    "जय हिंद", "सत श्री अकाल"
]

FAREWELL = ["धन्यवाद", "बाय", "अलविदा", "ठीक है", "बंद करो"]


# ════════════════════════════════════════════════════════════
#   MAIN FUNCTION — samjho()
#   This is called from main.py with the farmer's question
# ════════════════════════════════════════════════════════════

def samjho(question, city="Jodhpur"):
    """
    Understand the farmer's Hindi question and return a Hindi answer.

    10 categories handled:
    1.  Greeting         — नमस्ते, राम राम
    2.  Weather          — मौसम, तापमान, गर्मी, ठंड
    3.  Rain forecast    — बारिश, वर्षा, बादल
    4.  Mandi price      — भाव, दाम, कीमत, मंडी
    5.  Crop info        — फसल, बुआई, कब लगाएं
    6.  Soil advice      — मिट्टी, ज़मीन
    7.  Fertilizer       — खाद, यूरिया, डीएपी
    8.  Irrigation       — सिंचाई, पानी, ड्रिप
    9.  Pest control     — कीट, बीमारी, कीटनाशक
    10. Govt schemes     — योजना, सब्सिडी, बीमा, लोन
    +   Farewell         — धन्यवाद, बाय
    """

    if not question or question.strip() == "":
        return "कृपया कोई सवाल पूछें।"

    q = question.lower().strip()

    # ── 1. Farewell ───────────────────────────────────────
    for word in FAREWELL:
        if word in q:
            return "धन्यवाद! खेती में शुभकामनाएं। जय किसान!"

    # ── 2. Greeting ───────────────────────────────────────
    for word in GREETINGS:
        if word in q:
            return (
                "नमस्ते किसान भाई! मैं किसान सहायक हूँ। "
                "आप मौसम, बारिश, फसल, मंडी भाव, "
                "खाद, सिंचाई या सरकारी योजना के बारे में पूछ सकते हैं।"
            )

    # ── 3. Rain / Forecast ────────────────────────────────
    rain_words = ["बारिश", "वर्षा", "बादल", "पानी बरसेगा", "बरसात",
                  "मेह", "झड़ी", "आंधी", "तूफान"]
    if any(w in q for w in rain_words):
        from weather import barish_hogi
        return barish_hogi(city)

    # ── 4. Weather / Temperature ──────────────────────────
    weather_words = ["मौसम", "तापमान", "गर्मी", "ठंड", "धूप",
                     "हवा", "कोहरा", "धुंध", "आज कैसा", "ठंडक"]
    if any(w in q for w in weather_words):
        from weather import mausam_batao
        return mausam_batao(city)

    # ── 5. Mandi Price ────────────────────────────────────
    mandi_words = ["भाव", "दाम", "कीमत", "मंडी", "रेट", "बिकेगा",
                   "बेचूं", "खरीदूं", "महंगा", "सस्ता"]
    if any(w in q for w in mandi_words):
        # Check which crop they're asking about
        for crop, info in MANDI_PRICES.items():
            if crop in q:
                return (
                    f"{info['city']} में आज {crop} का भाव "
                    f"{info['price']} रुपये {info['unit']} है।"
                )
        # No specific crop found — list top 5
        reply = "आज के मंडी भाव: "
        top = list(MANDI_PRICES.items())[:5]
        parts = [f"{c}: ₹{i['price']}" for c, i in top]
        reply += ", ".join(parts) + "। किस फसल का भाव चाहिए, बताएं।"
        return reply

    # ── 6. Crop Info / Sowing ─────────────────────────────
    crop_words = ["फसल", "बुआई", "कब लगाएं", "कब बोएं", "खेती",
                  "कटाई", "रबी", "खरीफ", "बीज", "उगाएं"]
    if any(w in q for w in crop_words):
        for crop, info in FASAL_JANKARI.items():
            if crop in q:
                return info
        return (
            "आप किस फसल के बारे में जानना चाहते हैं? "
            "गेहूं, बाजरा, सरसों, चना, मक्का, मूंग, "
            "कपास या जीरा — बताएं।"
        )

    # ── 7. Soil Advice ────────────────────────────────────
    soil_words = ["मिट्टी", "ज़मीन", "भूमि", "मिट्टी जांच",
                  "काली", "लाल", "रेतीली", "दोमट", "चिकनी"]
    if any(w in q for w in soil_words):
        for soil, info in MITTI_JANKARI.items():
            if any(part in q for part in soil.split()):
                return info
        return (
            "मिट्टी जांच के लिए नज़दीकी कृषि विज्ञान केंद्र जाएं। "
            "जांच मुफ्त होती है। "
            "काली, लाल, रेतीली या दोमट मिट्टी के बारे में पूछें।"
        )

    # ── 8. Fertilizer Advice ──────────────────────────────
    fertilizer_words = ["खाद", "उर्वरक", "यूरिया", "डीएपी", "डी ए पी",
                        "पोटाश", "जैविक", "नीम खाद", "खाद कब दें"]
    if any(w in q for w in fertilizer_words):
        for khad, info in KHAD_JANKARI.items():
            if khad in q:
                return info
        return (
            "सही खाद फसल पर निर्भर करती है। "
            "गेहूं में यूरिया और डीएपी, "
            "सब्ज़ियों में जैविक खाद अच्छी रहती है। "
            "कौन सी खाद के बारे में जानना है?"
        )

    # ── 9. Irrigation ─────────────────────────────────────
    irrigation_words = ["सिंचाई", "पानी दें", "ड्रिप", "नहर",
                        "कुआं", "बोरवेल", "पंप", "पानी कब दें"]
    if any(w in q for w in irrigation_words):
        import random
        return random.choice(SINCHAI_JANKARI)

    # ── 10. Pest Control ──────────────────────────────────
    pest_words = ["कीट", "बीमारी", "कीटनाशक", "दवाई", "फसल खराब",
                  "पत्ते पीले", "इल्ली", "टिड्डी", "फफूंद", "रोग"]
    if any(w in q for w in pest_words):
        import random
        return random.choice(KEET_JANKARI)

    # ── 11. Government Schemes ────────────────────────────
    scheme_words = ["योजना", "सब्सिडी", "बीमा", "लोन", "क्रेडिट",
                    "सरकार", "पैसा", "मुआवज़ा", "रजिस्टर", "पीएम किसान"]
    if any(w in q for w in scheme_words):
        for scheme, info in YOJANA_JANKARI.items():
            if any(part in q for part in scheme.split()):
                return info
        # List all schemes
        schemes_list = ", ".join(YOJANA_JANKARI.keys())
        return (
            f"सरकारी योजनाएं: {schemes_list}। "
            f"किस योजना के बारे में जानना है?"
        )

    # ── Default — question not understood ─────────────────
    return _default_reply(q)


def _default_reply(question):
    """
    Called when no keyword matched.
    Gives a helpful suggestion in Hindi.
    """
    return (
        "माफ करें, मैं यह सवाल नहीं समझ पाया। "
        "आप इनके बारे में पूछ सकते हैं: "
        "मौसम, बारिश, मंडी भाव, फसल की जानकारी, "
        "मिट्टी, खाद, सिंचाई, कीट, या सरकारी योजना।"
    )


# ─── Run directly to test all 10 categories ───────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KISAN SAHAYAK — BRAIN MODULE TEST")
    print("=" * 55)

    test_questions = [
        ("Greeting",       "नमस्ते भाई"),
        ("Weather",        "आज का मौसम कैसा है"),
        ("Rain",           "क्या बारिश होगी"),
        ("Mandi - wheat",  "गेहूं का भाव क्या है"),
        ("Mandi - all",    "आज मंडी में दाम क्या है"),
        ("Crop info",      "सरसों कब बोएं"),
        ("Soil",           "रेतीली मिट्टी में क्या उगाएं"),
        ("Fertilizer",     "यूरिया कब डालें"),
        ("Irrigation",     "सिंचाई कैसे करें"),
        ("Pest",           "फसल में कीट लग गए"),
        ("Govt scheme",    "पीएम किसान योजना क्या है"),
        ("Farewell",       "धन्यवाद"),
        ("Unknown",        "अंतरिक्ष में क्या होता है"),
    ]

    for category, question in test_questions:
        print(f"\n[{category}]")
        print(f"  QUESTION: {question}")
        answer = samjho(question)
        print(f"  ANSWER:   {answer}")

    print("\n" + "=" * 55)
    print("  All 10 categories tested!")
    print("=" * 55)
