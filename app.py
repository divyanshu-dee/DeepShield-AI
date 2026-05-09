from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import requests
import cv2
import os

app = Flask(__name__)

# ======================================
# UPLOAD FOLDER
# ======================================
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ======================================
# ALLOWED FILES
# ======================================
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg',
    'mp4', 'avi', 'mov'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ======================================
# HUGGINGFACE CONFIG
# ======================================

# PUT YOUR NEW TOKEN HERE
API_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
    "https://router.huggingface.co/"
    "hf-inference/models/umm-maybe/AI-image-detector"
)

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/octet-stream"
}

# ======================================
# IMAGE DETECTION
# ======================================
def detect_ai_image(image_path):

    try:

        with open(image_path, "rb") as f:
            image_data = f.read()

        response = requests.post(
            API_URL,
            headers=HEADERS,
            data=image_data,
            timeout=120
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text[:500])

        # API ERROR
        if response.status_code != 200:

            if response.status_code == 401:
                return "⚠️ Invalid API Token", 0

            elif response.status_code == 503:
                return "⏳ Model Loading - Try Again", 0

            else:
                return "⚠️ API Error", 0

        # Convert response
        result = response.json()

        print("JSON:", result)

        # Check result format
        if isinstance(result, list):

            top = result[0]

            label = top.get("label", "Unknown")
            score = round(top.get("score", 0) * 100, 2)

            print("LABEL:", label)
            print("SCORE:", score)

            # AI or Real
            if (
                "ai" in label.lower()
                or "fake" in label.lower()
                or "generated" in label.lower()
            ):

                final_label = "🤖 AI Generated"

            else:
                final_label = "✅ Real"

            return final_label, score

        return "⚠️ Detection Failed", 0

    except Exception as e:

        print("ERROR:", e)

        return "⚠️ Detection Failed", 0

# ======================================
# VIDEO DETECTION
# ======================================
def detect_ai_video(video_path):

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    scores = []

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        # Analyze every 30th frame
        if frame_count % 30 == 0:

            temp_frame = os.path.join(
                app.config['UPLOAD_FOLDER'],
                "temp_frame.jpg"
            )

            cv2.imwrite(temp_frame, frame)

            try:

                label, score = detect_ai_image(temp_frame)

                if score > 0:
                    scores.append(score)

            except:
                pass

        frame_count += 1

    cap.release()

    if len(scores) == 0:
        return "⚠️ Could Not Analyze", 0

    avg_score = sum(scores) / len(scores)

    if avg_score > 60:
        return "🤖 AI Generated Video", round(avg_score, 2)

    return "✅ Real Video", round(avg_score, 2)

# ======================================
# MAIN ROUTE
# ======================================
@app.route('/', methods=['GET', 'POST'])
def index():

    result = None
    filename = None
    error = None
    filetype = None

    if request.method == 'POST':

        # Check upload
        if 'file' not in request.files:

            error = "No file uploaded!"

            return render_template(
                'index.html',
                error=error
            )

        file = request.files['file']

        # Empty filename
        if file.filename == '':

            error = "No file selected!"

            return render_template(
                'index.html',
                error=error
            )

        # Valid file
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            file.save(path)

            ext = filename.rsplit('.', 1)[1].lower()

            # IMAGE
            if ext in ['png', 'jpg', 'jpeg']:

                filetype = 'image'

                label, score = detect_ai_image(path)

            # VIDEO
            else:

                filetype = 'video'

                label, score = detect_ai_video(path)

            result = f"{label} ({score}%)"

        else:

            error = (
                "Only JPG, JPEG, PNG, MP4, AVI, MOV files are allowed!"
            )

    return render_template(
        'index.html',
        result=result,
        filename=filename,
        error=error,
        filetype=filetype
    )

# ======================================
# RUN APP
# ======================================
if __name__ == '__main__':
    app.run(debug=True)