# ============================================================
#  main.py — Hindi Voice Assistant (Kisan Sahayak)
#  Flask web server + voice loop combined
#  Run: python main.py
#  Then open: http://localhost:5000 in your browser
#  Author: Your Name | College Project
# ============================================================

from flask import Flask, render_template, request, jsonify, send_file
import threading
import os
import io
import time
import json
from datetime import datetime
import sys

# Windows Unicode console fix
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# Import our custom modules
from brain import samjho
# Weather functions imported dynamically in routes to avoid caching issues

# gTTS for text-to-speech in web mode
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[WARN] gTTS not installed. Voice output disabled in web mode.")
    print("[TIP]  Run: pip install gTTS")

# SpeechRecognition for microphone mode
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("[WARN] SpeechRecognition not installed. Mic mode disabled.")

# ─── Flask App Setup ──────────────────────────────────────────
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False   # important for Hindi text in JSON

# ─── Settings ─────────────────────────────────────────────────
DEFAULT_CITY    = "Jodhpur"
HOST            = "0.0.0.0"    # 0.0.0.0 = accessible on local network
PORT            = 5000
DEBUG           = True         # set False when done testing
CHAT_HISTORY    = []           # stores conversation in memory
MAX_HISTORY     = 50           # max messages to keep
# ─────────────────────────────────────────────────────────────


# ════════════════════════════════════════════════════════════
#   WEB ROUTES
# ════════════════════════════════════════════════════════════

@app.route("/")
def home():
    """Serve the main web interface."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Main API endpoint.
    Receives a Hindi question (text), returns Hindi answer (text + audio).

    Request JSON:  { "question": "आज का मौसम कैसा है", "city": "Jodhpur" }
    Response JSON: { "answer": "जोधपुर में आज...", "success": true }
    """
    try:
        data     = request.get_json()
        question = data.get("question", "").strip()
        city     = data.get("city", DEFAULT_CITY).strip()

        if not question:
            return jsonify({
                "success": False,
                "answer":  "कृपया कोई सवाल पूछें।"
            })

        # Get answer from brain
        answer = samjho(question, city)

        # Save to chat history
        _save_to_history(question, answer)

        return jsonify({
            "success":  True,
            "answer":   answer,
            "question": question,
            "time":     datetime.now().strftime("%I:%M %p")
        })

    except Exception as e:
        print(f"[ERROR] /ask endpoint error: {e}")
        return jsonify({
            "success": False,
            "answer":  "कुछ गड़बड़ हो गई। कृपया दोबारा पूछें।"
        }), 500


@app.route("/speak", methods=["POST"])
def speak():
    """
    Text-to-Speech endpoint.
    Receives Hindi text, returns MP3 audio file.

    Request JSON:  { "text": "नमस्ते किसान भाई" }
    Response:      MP3 audio stream
    """
    if not TTS_AVAILABLE:
        return jsonify({"error": "gTTS not installed"}), 503

    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Generate Hindi speech
        tts = gTTS(text=text, lang="hi", slow=False)

        # Save to memory buffer (no temp file needed)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return send_file(
            audio_buffer,
            mimetype="audio/mpeg",
            as_attachment=False
        )

    except Exception as e:
        print(f"[ERROR] /speak endpoint error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/weather", methods=["GET"])
def weather():
    """Quick weather endpoint for dashboard widget."""
    print("[DEBUG] Weather endpoint called")
    city = request.args.get("city", DEFAULT_CITY)
    try:
        # Import dynamically to avoid caching issues
        from weather import mausam_batao, barish_hogi
        current  = mausam_batao(city)
        forecast = barish_hogi(city)
        return jsonify({
            "success":  True,
            "current":  current,
            "forecast": forecast,
            "city":     city
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/history", methods=["GET"])
def history():
    """Return chat history as JSON."""
    return jsonify({
        "success": True,
        "history": CHAT_HISTORY[-20:]   # last 20 messages
    })


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Clear chat history."""
    global CHAT_HISTORY
    CHAT_HISTORY = []
    return jsonify({"success": True, "message": "History cleared."})


@app.route("/status", methods=["GET"])
def status():
    """Health check — tells frontend which features are available."""
    return jsonify({
        "success":        True,
        "tts_available":  TTS_AVAILABLE,
        "mic_available":  SR_AVAILABLE,
        "server_time":    datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "default_city":   DEFAULT_CITY,
        "version":        "1.0.0"
    })


# ════════════════════════════════════════════════════════════
#   VOICE LOOP (runs in background thread)
#   Only starts if microphone is available
# ════════════════════════════════════════════════════════════

def voice_loop():
    """
    Background thread — listens to microphone continuously.
    Works alongside the web interface.
    Farmer can use BOTH voice and web at the same time.
    """
    if not SR_AVAILABLE:
        print("[INFO] Voice loop skipped — SpeechRecognition not installed.")
        return

    from speech import sun_lo, bolo

    print("\n[VOICE] Voice loop started. Speak in Hindi anytime.")
    bolo("नमस्ते! किसान सहायक तैयार है। बोलिए।")

    while True:
        try:
            question = sun_lo()

            if question:
                print(f"[VOICE] Heard: {question}")
                answer = samjho(question, DEFAULT_CITY)
                print(f"[VOICE] Answer: {answer}")
                bolo(answer)
                _save_to_history(question, answer, source="voice")

            time.sleep(0.5)   # small pause between listens

        except KeyboardInterrupt:
            print("[VOICE] Voice loop stopped.")
            break
        except Exception as e:
            print(f"[VOICE] Error in voice loop: {e}")
            time.sleep(2)     # wait before retrying


# ════════════════════════════════════════════════════════════
#   HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════

def _save_to_history(question, answer, source="web"):
    """Save a Q&A pair to in-memory chat history."""
    global CHAT_HISTORY

    CHAT_HISTORY.append({
        "question": question,
        "answer":   answer,
        "source":   source,
        "time":     datetime.now().strftime("%I:%M %p")
    })

    # Keep history from growing too large
    if len(CHAT_HISTORY) > MAX_HISTORY:
        CHAT_HISTORY = CHAT_HISTORY[-MAX_HISTORY:]


def print_startup_banner():
    """Show helpful startup info in terminal."""
    print("\n" + "=" * 55)
    print("   KISAN SAHAYAK — किसान सहायक")
    print("   Hindi Voice Assistant for Farmers")
    print("=" * 55)
    print(f"   Web Interface : http://localhost:{PORT}")
    print(f"   Network Access: http://YOUR_IP:{PORT}")
    print(f"   Default City  : {DEFAULT_CITY}")
    print(f"   TTS (Voice)   : {'YES' if TTS_AVAILABLE else 'NO — pip install gTTS'}")
    print(f"   Microphone    : {'YES' if SR_AVAILABLE else 'NO — pip install SpeechRecognition'}")
    print("=" * 55)
    print("   Press CTRL+C to stop the server")
    print("=" * 55 + "\n")


# ════════════════════════════════════════════════════════════
#   START THE SERVER
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print_startup_banner()

    # Start voice loop in background (only if mic is available)
    if SR_AVAILABLE:
        voice_thread = threading.Thread(target=voice_loop, daemon=True)
        voice_thread.start()
        print("[INFO] Voice loop running in background thread.")
    else:
        print("[INFO] Running in web-only mode (no microphone).")

    # Start Flask web server
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)
