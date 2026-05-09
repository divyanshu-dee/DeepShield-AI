# 🚀 DeepShield AI

DeepShield AI is a web-based platform that detects whether an image or video is AI-generated or real using AI-powered analysis.

The project uses the HuggingFace Inference API for AI image detection and supports both image and video uploads through a Flask backend.

---

# 🌟 Features

- 📸 AI Image Detection
- 🎥 AI Video Detection
- 🤖 HuggingFace AI Integration
- ☁️ Cloud Deployment Ready
- 🔒 Secure API Token Handling
- ⚡ Flask Backend
- 🖥️ User-Friendly Interface

---

# 🧠 How It Works

## Image Detection
1. User uploads image
2. Backend sends image to HuggingFace API
3. AI model analyzes image
4. Result + confidence score displayed

## Video Detection
1. User uploads video
2. Frames extracted using OpenCV
3. Selected frames analyzed
4. Average confidence score generated

---

# 🛠️ Tech Stack

## Frontend
- HTML
- CSS

## Backend
- Python
- Flask

## AI / ML
- HuggingFace Inference API

## Libraries
- OpenCV
- Requests
- NumPy

## Deployment
- Render

---

# 📂 Project Structure

```bash
DeepShield-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── uploads/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/divyanshu-dee/DeepShield-AI.git
```

## Open Folder

```bash
cd DeepShield-AI
```

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variable Setup

Create a HuggingFace token from:
https://huggingface.co/settings/tokens

## Windows PowerShell

```powershell
$env:HF_TOKEN="your_token_here"
python app.py
```

## Windows CMD

```cmd
set HF_TOKEN=your_token_here
python app.py
```

---

# ▶️ Run Project

```bash
python app.py
```

Open:
```bash
http://127.0.0.1:5000
```

---

# ☁️ Render Deployment

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
gunicorn app:app
```

## Environment Variable

| Key | Value |
|---|---|
| HF_TOKEN | Your HuggingFace Token |

---

# 📸 Supported Files

## Images
- JPG
- JPEG
- PNG

## Videos
- MP4
- AVI
- MOV

---

# 🚀 Future Improvements

- Better deepfake detection
- Frame-by-frame video analysis
- Real-time webcam detection
- User authentication
- Detection history

---

# 👨‍💻 Author

Divyanshu Vishwakarma

Aspiring Engineer | AI & ECE Enthusiast

---

# 📌 Note

This project is a prototype and AI detection results may not always be 100% accurate.

---

# 🔗 Links

## GitHub
https://github.com/divyanshu-dee/DeepShield-AI

## Live Demo
https://deepshield-ai-yrhc.onrender.com/
# Run the app
python app.py
