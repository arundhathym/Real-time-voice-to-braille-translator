<div align="center">

# 🎙️ Real-Time Voice to Braille Translator

### A Flask web application that converts live speech into Braille — supporting both English and Malayalam — powered by OpenAI Whisper AI.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI_Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

---

## 📖 About The Project

The **Real-Time Voice to Braille Translator** is a full-stack web application that records audio directly from the browser, transcribes it using OpenAI's **Whisper AI model**, and converts the output into Braille characters — live, in the browser.

What makes this project stand out is its **bilingual Braille support** — it handles both **English** and **Malayalam**, with a custom-built character mapping covering the complete Malayalam script including vowels, consonants, vowel signs (matras), virama, anuswara, and visarga.

Built with accessibility at its core, this project bridges the gap between spoken language and Braille for visually impaired users — entirely through a browser interface.

---

## ✨ Features

- 🎤 **Live Voice Input** — captures audio from the browser in `.webm` format via the MediaRecorder API
- 🤖 **AI-Powered Transcription** — uses OpenAI Whisper (`medium` model) for high-accuracy speech-to-text
- ⠿ **Real-Time Braille Output** — instantly converts transcribed text to Grade 1 Braille Unicode
- 🌐 **Bilingual Support** — handles both **English** (`en`) and **Malayalam** (`ml`) speech
- 🧠 **Custom Malayalam Braille Engine** — covers independent vowels, matras, consonants, virama (്), anuswara (ം), and visarga (ഃ)
- ⚡ **Auto GPU Detection** — Whisper runs on CUDA (NVIDIA) → Apple MPS → CPU, whichever is available
- 🔊 **FFmpeg Audio Pipeline** — processes raw browser audio before Whisper inference
- 🧹 **Automatic Temp File Cleanup** — audio files are deleted from disk after each transcription

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **AI / Speech Recognition** | OpenAI Whisper (medium model) |
| **Deep Learning** | PyTorch (CUDA / MPS / CPU) |
| **Audio Processing** | FFmpeg, ffmpeg-python |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Braille Engine** | Custom Python mapping — English + Malayalam |

---

## ⚙️ How It Works

```
🎤  User speaks into browser
         │
         ▼
   Audio saved as temp .webm file
         │
         ▼
   Flask  POST /convert  receives file + language param
         │
         ▼
   Whisper medium model transcribes audio
   (language: "en" → English | "ml" → Malayalam)
         │
         ▼
   braille_conerter.py maps each character → Braille Unicode
         │
         ▼
   ⠓⠑⠇⠇⠕  Braille output returned as JSON → displayed in browser
         │
         ▼
   Temp audio file deleted from disk
```

---

## 📂 Project Structure

```
Real-time-voice-to-braille-translator/
├── app.py                  # Flask app — routes, Whisper loading, GPU logic, /convert endpoint
├── braille_conerter.py     # Braille character map + text_to_braille() conversion function
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Frontend — UI, audio recording, fetch calls
└── static/                 # CSS and JavaScript assets
```

---

## 🌐 Braille Language Support

### English — Full A–Z Alphabet (Grade 1)
`a`→⠁ `b`→⠃ `c`→⠉ `d`→⠙ `e`→⠑ `f`→⠋ `g`→⠛ `h`→⠓ `i`→⠊ `j`→⠚
`k`→⠅ `l`→⠇ `m`→⠍ `n`→⠝ `o`→⠕ `p`→⠏ `q`→⠟ `r`→⠗ `s`→⠎ `t`→⠞
`u`→⠥ `v`→⠧ `w`→⠺ `x`→⠭ `y`→⠽ `z`→⠵

**Punctuation:** `.`→⠲ `,`→⠂ `?`→⠦ `!`→⠖ `"`→⠶ `'`→⠄ `-`→⠤ `(`→⠐⠣ `)`→⠐⠜

### Malayalam — Complete Script Coverage

| Category | Characters |
|---|---|
| Independent Vowels | അ ആ ഇ ഈ ഉ ഊ ഋ എ ഏ ഐ ഒ ഓ ഔ |
| Vowel Signs (Matras) | ാ ി ീ ു ൂ ൃ െ േ ൈ ൊ ോ ൌ |
| Consonants | ക ഖ ഗ ഘ ങ ച ഛ ജ ഝ ഞ ട ഠ ഡ ഢ ണ ത ഥ ദ ധ ന പ ഫ ബ ഭ മ യ ര ല വ ശ ഷ സ ഹ ള ഴ റ |
| Special Signs | ് (Virama) · ം (Anuswara) · ഃ (Visarga) |

---

## ⚡ GPU Auto-Selection

```python
# From app.py — device is selected automatically at startup
if torch.cuda.is_available():      → CUDA  (NVIDIA GPU — fastest)
elif torch.backends.mps.is_available(): → MPS (Apple M1/M2/M3)
else:                              → CPU  (works on any machine)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- FFmpeg installed and added to system PATH
- (Optional) CUDA GPU for faster transcription

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/arundhathym/Real-time-voice-to-braille-translator.git
cd Real-time-voice-to-braille-translator

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Verify FFmpeg is available
ffmpeg -version

# 4. Run the Flask app
python app.py
```

Then open **http://localhost:5000** in your browser.

> ⚠️ Best experienced in **Google Chrome** — full MediaRecorder API support required.

---

## 📦 Dependencies

```
flask
torch
openai-whisper
ffmpeg-python
setuptools
```

---

## 🔮 Future Scope

- [ ] Grade 2 (contracted) Braille support
- [ ] Number-to-Braille mapping
- [ ] Support for more Indian languages
- [ ] Mobile-responsive UI
- [ ] Downloadable Braille output as `.txt`

---

## 🙋‍♀️ Developer

**Arundhathy Mohan**
MCA Graduate | Full Stack Developer
College of Engineering Chengannur, APJ Abdul Kalam Technological University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arundhathy)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/arundhathym)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white)](mailto:arundhathymohan2003@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
⭐ Star this repo if you believe in making technology more accessible!
</div>
