🎯 Live Video QR + Face Verification System
🧠 Overview

This project implements a real-time user authentication system using QR code scanning and facial recognition.
It verifies a person’s identity using a live webcam feed and a MongoDB database.

⚙️ Features

📸 Live face capture and embedding extraction using DeepFace

🔒 QR code generation for unique user identification

🧩 Face verification with cosine similarity

🧠 MongoDB database integration for user and log storage

🎥 Real-time video verification via OpenCV

🧩 Tech Stack
Component	Technology Used
Face Recognition	DeepFace (Facenet)
QR Code	qrcode (PIL)
Video Stream	OpenCV
Database	MongoDB Atlas
Machine Learning Metric	Cosine Similarity
Language	Python
🧰 Installation
git clone https://github.com/<your-username>/live-video-qr-face-verification.git
cd live-video-qr-face-verification
pip install -r requirements.txt

🚀 Usage

Run the system:

python main.py


Main Menu

1. Register new user (live video)
2. Verify user (live video)
3. Exit

🗃️ MongoDB Setup

Create a cluster on MongoDB Atlas

Get your connection string and replace it in:

MONGO_URI = "your_mongo_connection_string"


Collections used:

users → stores user info + face embedding + QR data

logs → stores access logs

📂 Folder Structure
live-video-qr-face-verification/
│
├── main.py
├── requirements.txt
├── README.md
├── generated_qr/          # QR codes saved here
├── faces_detected/        # Captured faces
├── qr_detected/           # (optional future use)
└── .gitignore             # optional

📸 Demo Idea (Optional)

You can add a demo GIF or video later showing:

User registration

QR + Face verification working live

⚡ Future Enhancements

Add admin dashboard for access logs

Multi-user face recognition (top match)

Deploy as a desktop or web app (Flask/Streamlit)

Integrate with IoT gate lock system
