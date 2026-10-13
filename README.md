# 🚗 Driver Drowsiness Detection System

A real-time Driver Drowsiness Detection System built with Python, OpenCV, and Flask to monitor a driver's eye movements and detect signs of drowsiness. When prolonged eye closure is detected, the system triggers an audio alert to help improve driver safety.

## ✨ Features

- 👁️ **Real-Time Eye Monitoring** — Uses facial landmarks to monitor eye movements through a camera.
- 🧠 **Drowsiness Detection** — Uses the Eye Aspect Ratio (EAR) technique to detect prolonged eye closure.
- 🔊 **Audio Alert System** — Plays an alarm when drowsiness is detected.
- 🌐 **Web-Based Interface** — Flask-powered application with login, signup, dashboard, and detection pages.
- 🔐 **User Authentication** — Provides account registration and login functionality.
- 📊 **Dashboard** — Access the application's detection features through a dashboard.
- 🎨 **Responsive UI** — Custom HTML, CSS, and JavaScript frontend.
- 🗄️ **Database Integration** — Database configuration and application data management.

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **OpenCV**
- **dlib**
- **NumPy**
- **SciPy**
- **Pygame**
- **HTML, CSS, JavaScript**
- **Database:** As configured in the application

## 📂 Project Structure

```text
drowsiness_detection/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   ├── admin_dashboard.css
│   │   │   ├── dashboard.css
│   │   │   ├── detection.css
│   │   │   ├── login.css
│   │   │   ├── logout.css
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── dashboard.js
│   │   │   └── script.js
│   │   └── images/
│   ├── templates/
│   │   ├── admin_dashboard.html
│   │   ├── dashboard.html
│   │   ├── detection.html
│   │   ├── login.html
│   │   ├── logout.html
│   │   └── signup.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   ├── routes.py
│   │   ├── shape_predictor_68_face_landmarks.dat
│   │   └── music.wav
│   └── __init__.py
├── database/
│   └── db_config.py
├── .gitattributes
├── README.md
├── requirements.txt
└── run.py
```

*The structure above reflects your shown folders and the requested model and audio files. Adjust filenames and locations to match your actual project.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shahidshaikh-18/drowsiness_detection.git
cd drowsiness_detection
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

Ensure your requirements include the libraries actually used by your code, such as Flask, OpenCV, dlib, NumPy, SciPy, and Pygame.

### 4. Add the facial landmark model

Download the official dlib 68-point facial landmark predictor model from the [dlib model files](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) page.

Extract the compressed file and place it at the path expected by your application:

```text
app/utils/shape_predictor_68_face_landmarks.dat
```

The model is required for facial landmark detection if your code loads it from this location.

### 5. Add the audio alert

Place your audio file in the expected location:

```text
app/utils/music.wav
```

Make sure the filename and extension match the path configured in your Python code.

### 6. Run the application

```powershell
python run.py
```

Open the local URL shown in the terminal.

## 🔍 How It Works

1. The application accesses the camera to capture video frames.
2. Face detection and facial landmark analysis identify eye regions.
3. The Eye Aspect Ratio (EAR) is calculated to estimate whether the eyes are closed.
4. Prolonged eye closure triggers an audio alarm.
5. The web interface provides access to the detection functionality.

## 🧪 Testing

- Test with eyes open and closed.
- Verify that prolonged eye closure triggers an alert.
- Confirm camera permissions and video feed functionality.
- Verify that the facial landmark model loads correctly.
- Check that the alarm plays when detection is triggered.
- Test login, signup, and dashboard functionality.

## 🔐 Security and Privacy

- Use secure password hashing for user account passwords.
- Keep secret keys and database credentials out of source control.
- Obtain permission before accessing a camera.
- Avoid storing camera footage or personal data unnecessarily.

## 🚀 Future Enhancements

- Improve detection accuracy under different lighting conditions.
- Add configurable alert thresholds.
- Record detection events and generate reports.
- Add configurable alarm settings.
- Improve dashboard analytics and usability.

## ⚠️ Disclaimer

This project is intended for educational purposes and driver-safety research. It is an assistance tool, not a replacement for adequate rest or safe driving practices.

## 👨‍💻 Author

**Shahid Shaikh**

Aspiring Cybersecurity Analyst | Python Developer

