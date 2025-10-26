import os 
import tempfile
from flask import Flask, request, jsonify, render_template
import whisper
import logging
import subprocess 
import sys
import torch  # For GPU detection
from braille_converter import text_to_braille  # Import your converter

# --- Configuration ---
WHISPER_MODEL_NAME = "medium"  # 'medium' model gives better Malayalam accuracy
TEMP_DIR = tempfile.gettempdir()

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Flask app initialization
app = Flask(__name__)
model = None


# --- Determine Device (CPU / GPU / MPS) ---
def get_device():
    if torch.cuda.is_available():
        device = "cuda"
        logging.info("✅ Using CUDA GPU for model execution.")
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = "mps"
        logging.info("✅ Using Apple MPS GPU for model execution.")
    else:
        device = "cpu"
        logging.info("⚙️ Using CPU for model execution.")
    return device


# --- Home Page ---
@app.route("/")
def index():
    return render_template("index.html")


# --- Audio Conversion Endpoint ---
@app.route("/convert", methods=["POST"])
def convert_audio():
    global model
    if model is None:
        return jsonify({"error": "Speech recognition model not loaded."}), 500

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']
    language = request.form.get('language', 'ml')
    prompt = request.form.get('prompt', '')

    temp_input_webm_path = os.path.join(TEMP_DIR, f"input_{os.getpid()}.webm")

    try:
        # 1️⃣ Save the audio file
        audio_file.save(temp_input_webm_path)

        # 2️⃣ Prepare Whisper options
        language_code = "ml" if language == "ml" else "en"
        options = {
            "language": language_code,
            "initial_prompt": prompt,
            "fp16": False
        }

        # 3️⃣ Transcribe audio
        import time
        start_time = time.time()

        result = model.transcribe(temp_input_webm_path, **options)

        logging.info(f"⏱ Transcription completed in {time.time() - start_time:.2f}s")

        text = result.get("text", "").strip()
        logging.info(f"[DEBUG] Whisper Output: {repr(text)}")

        if not text:
            return jsonify({
                "text": "(No clear speech detected)",
                "braille": "—"
            })

        # 4️⃣ Convert text to Braille
        braille_text = text_to_braille(text, language)

        if not braille_text and text:
            braille_text = "Conversion resulted in limited Braille output (Map limitation)."

        return jsonify({
            "text": text,
            "braille": braille_text
        })

    except Exception as e:
        import traceback
        logging.error(f"❌ Transcription/Conversion failed: {e}")
        logging.error(traceback.format_exc())
        return jsonify({
            "error": f"Transcription error ({type(e).__name__}): {str(e)}"
        }), 500

    finally:
        # Cleanup temp file
        if os.path.exists(temp_input_webm_path):
            os.remove(temp_input_webm_path)


# --- FFmpeg Check ---
def check_ffmpeg_availability():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        logging.info("✅ FFmpeg check successful.")
        return True
    except FileNotFoundError:
        logging.critical("❌ FFmpeg not found. Please install and add it to PATH.")
        return False
    except Exception as e:
        logging.warning(f"⚠️ FFmpeg check issue: {e}")
        return True


# --- Model Loader ---
def load_model():
    global model
    if not check_ffmpeg_availability():
        sys.exit("FFmpeg missing — cannot continue.")

    try:
        device = get_device()
        logging.info(f"🚀 Loading Whisper model '{WHISPER_MODEL_NAME}' on {device} ...")
        model = whisper.load_model(WHISPER_MODEL_NAME, device=device)
        logging.info("✅ Whisper model loaded successfully.")
    except Exception as e:
        logging.critical(f"❌ Failed to load Whisper model: {e}")
        model = None


# --- Run App ---
if __name__ == '__main__':
    load_model()
    app.run(debug=True)
