# ============================================================
#  speech.py — Hindi Voice Assistant (Kisan Sahayak)
#  Listen to Hindi voice + Speak Hindi replies
#  Author: Your Name | College Project
# ============================================================

import speech_recognition as sr
from gtts import gTTS
import os
import sys
import time

# ─── Settings ────────────────────────────────────────────────
LANGUAGE        = "hi-IN"   # Hindi (India) for listening
TTS_LANGUAGE    = "hi"      # Hindi for speaking
AUDIO_FILE      = "reply.mp3"
MAX_RETRIES     = 3         # retry listening this many times
LISTEN_TIMEOUT  = 5         # seconds to wait for speech to start
PHRASE_LIMIT    = 10        # max seconds to record one phrase
# ─────────────────────────────────────────────────────────────


def sun_lo(retry_count=0):
    """
    Listen to the farmer's voice using the microphone.
    Returns the recognized Hindi text as a string.
    Returns None if listening fails.

    Handles these errors:
    - No microphone found
    - No speech detected (timeout)
    - Could not understand speech
    - No internet connection (Google API fails)
    """

    r = sr.Recognizer()

    # Adjust sensitivity — important for noisy farm environments
    r.energy_threshold = 300        # lower = more sensitive
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8         # seconds of silence = end of speech

    # ── Step 1: Check microphone is available ──────────────
    try:
        mic = sr.Microphone()
    except OSError:
        print("[ERROR] Microphone नहीं मिला। कृपया माइक्रोफोन लगाएं।")
        print("[ERROR] Microphone not found. Please connect a microphone.")
        return None

    # ── Step 2: Listen ─────────────────────────────────────
    with mic as source:
        print("\n[INFO] Adjusting for background noise... please wait.")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
        except Exception:
            pass  # not critical, continue anyway

        print("[READY] बोलिए... (Speak now...)")

        try:
            audio = r.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_LIMIT
            )
        except sr.WaitTimeoutError:
            print("[WARN] कोई आवाज़ नहीं सुनाई दी। फिर से बोलिए।")
            print("[WARN] No speech detected. Please try again.")

            # Auto-retry up to MAX_RETRIES times
            if retry_count < MAX_RETRIES:
                print(f"[INFO] Retry {retry_count + 1}/{MAX_RETRIES}...")
                time.sleep(1)
                return sun_lo(retry_count + 1)
            return None

    # ── Step 3: Convert audio to text (Google STT) ─────────
    print("[INFO] Recognizing...")
    try:
        text = r.recognize_google(audio, language=LANGUAGE)
        print(f"[HEARD] आपने कहा: {text}")
        return text

    except sr.UnknownValueError:
        print("[WARN] माफ करें, आपकी बात समझ नहीं आई। फिर से बोलिए।")
        print("[WARN] Could not understand speech. Please speak clearly.")
        if retry_count < MAX_RETRIES:
            time.sleep(1)
            return sun_lo(retry_count + 1)
        return None

    except sr.RequestError as e:
        print(f"[ERROR] इंटरनेट कनेक्शन नहीं है या Google API काम नहीं कर रहा।")
        print(f"[ERROR] Google Speech API error: {e}")
        print("[TIP]  Please check your internet connection.")
        return None

    except Exception as e:
        print(f"[ERROR] Unexpected error during recognition: {e}")
        return None


def bolo(text):
    """
    Convert Hindi text to speech and play it out loud.
    Uses Google Text-to-Speech (gTTS).

    Handles these errors:
    - No internet connection
    - Empty text
    - Audio playback failure
    """

    # ── Step 1: Validate input ─────────────────────────────
    if not text or text.strip() == "":
        print("[WARN] bolo() called with empty text. Nothing to speak.")
        return False

    print(f"[SPEAK] {text}")

    # ── Step 2: Generate audio file ────────────────────────
    try:
        tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
        tts.save(AUDIO_FILE)
    except Exception as e:
        print(f"[ERROR] Could not generate speech audio: {e}")
        print("[TIP]  Check internet connection for gTTS to work.")
        # Fallback: just print the text so user can read it
        print(f"[FALLBACK] Text reply: {text}")
        return False

    # ── Step 3: Play audio based on operating system ───────
    played = _play_audio(AUDIO_FILE)

    # ── Step 4: Clean up temp file ─────────────────────────
    try:
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)
    except Exception:
        pass  # not critical

    return played


def _play_audio(filepath):
    """
    Play an MP3 file. Tries multiple methods depending on OS.
    Returns True if successful, False if all methods fail.
    """

    if not os.path.exists(filepath):
        print(f"[ERROR] Audio file not found: {filepath}")
        return False

    platform = sys.platform

    # Windows
    if platform == "win32":
        try:
            os.system(f'start /wait "" "{filepath}"')
            return True
        except Exception as e:
            print(f"[ERROR] Windows audio playback failed: {e}")

    # macOS
    elif platform == "darwin":
        try:
            os.system(f'afplay "{filepath}"')
            return True
        except Exception as e:
            print(f"[ERROR] macOS audio playback failed: {e}")

    # Linux (Raspberry Pi, Ubuntu, etc.)
    elif platform.startswith("linux"):
        # Try mpg321 first (most common on Raspberry Pi)
        if os.system("which mpg321 > /dev/null 2>&1") == 0:
            try:
                os.system(f'mpg321 -q "{filepath}"')
                return True
            except Exception:
                pass

        # Try mpg123 (alternative)
        if os.system("which mpg123 > /dev/null 2>&1") == 0:
            try:
                os.system(f'mpg123 -q "{filepath}"')
                return True
            except Exception:
                pass

        # Try ffplay (comes with ffmpeg)
        if os.system("which ffplay > /dev/null 2>&1") == 0:
            try:
                os.system(f'ffplay -nodisp -autoexit -loglevel quiet "{filepath}"')
                return True
            except Exception:
                pass

        print("[ERROR] No audio player found on Linux.")
        print("[TIP]  Run: sudo apt install mpg321")
        return False

    else:
        print(f"[ERROR] Unknown platform: {platform}")
        return False


def test_microphone():
    """
    Quick test to check if microphone is working.
    Call this before running main.py.
    """
    print("=" * 50)
    print("MICROPHONE TEST")
    print("=" * 50)

    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            print("[FAIL] No microphones found on this system.")
            return False

        print(f"[OK]   Found {len(mics)} microphone(s):")
        for i, name in enumerate(mics):
            print(f"       [{i}] {name}")

        print("\n[INFO] Testing default microphone for 2 seconds...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"[OK]   Microphone working! Energy level: {int(r.energy_threshold)}")

        print("[PASS] Microphone test passed!\n")
        return True

    except OSError as e:
        print(f"[FAIL] Microphone error: {e}")
        return False


# ─── Run directly to test ─────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  KISAN SAHAYAK — SPEECH MODULE TEST")
    print("=" * 50)

    # Test 1: Check microphone
    mic_ok = test_microphone()

    if mic_ok:
        # Test 2: Speak a greeting
        print("\n[TEST] Testing Hindi speech output...")
        bolo("नमस्ते! मैं किसान सहायक हूँ। आपकी सेवा में तैयार हूँ।")

        # Test 3: Listen once
        print("\n[TEST] Testing Hindi speech input...")
        print("[ACTION] Please say something in Hindi now...")
        result = sun_lo()

        if result:
            print(f"\n[SUCCESS] Speech module working!")
            print(f"[RESULT]  You said: {result}")
            bolo(f"आपने कहा: {result}")
        else:
            print("\n[FAIL] Could not recognize speech. Check microphone and internet.")
    else:
        print("\n[SKIP] Skipping speech tests — microphone not available.")
        print("[TIP]  Install PyAudio: pip install pyaudio")
        print("[TIP]  On Linux: sudo apt install portaudio19-dev")