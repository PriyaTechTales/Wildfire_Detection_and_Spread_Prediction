# Wildfire Detection and Spread Prediction

This project is a full-stack web application designed to assist in early *wildfire detection* and *predict the potential spread* of fire. It integrates *deep learning (YOLOv8)* for detecting fire/smoke and *machine learning (Random Forest Regressor)* for predicting fire spread using environmental conditions.

> *Tech Stack:* Django | HTML | CSS | JavaScript | YOLOv8 | Random Forest | SQLite

---

## 🚀 Features

- *Fire Detection using YOLOv8*
  - Detects Fire, Smoke, or No Fire in uploaded images.
  - Uses deep learning for real-time prediction with confidence scores.

- *Spread Prediction using ML*
  - Predicts wildfire spread area and intensity using environmental parameters.
  - Powered by Random Forest Regressor for accurate regression predictions.

- *Frontend*
  - Built with *HTML, **CSS, and **JavaScript* for responsiveness and interactivity.

- *Backend*
  - Developed using *Django* for robust server-side logic and secure data flow.

- *Database*
  - Uses *SQLite* to store user data, results, and logs.

- *Visualizations*
  - Interactive graphs to show prediction trends and detection results.

---

## 🧠 How It Works

### 1. Wildfire Detection
- User uploads an image.
- YOLOv8 model detects fire, smoke, or no fire.
- Results are shown with bounding boxes and confidence percentages.

### 2. Spread Prediction
- User fills a form with inputs like temperature, wind speed, humidity, etc.
- ML model returns predicted wildfire spread in square meters.
- Result is displayed with visual aid.

---

## 🛠 Technology Stack

| Layer      | Tools Used                            |
|------------|----------------------------------------|
| Frontend   | HTML, CSS, JavaScript                  |
| Backend    | Django (v4.x or higher)                |
| Database   | SQLite                                 |
| ML Model   | Random Forest Regressor (scikit-learn) |
| DL Model   | YOLOv8 (Ultralytics)                   |

---

## 📦 Requirements

### Python: 3.10+  
### Django: 4.x+

### Python Libraries:
```bash
numpy>=1.21.0  
pandas>=1.3.0  
scikit-learn>=1.0.0  
joblib>=1.2.0  
ultralytics>=8.0.0  
opencv-python>=4.5.0
