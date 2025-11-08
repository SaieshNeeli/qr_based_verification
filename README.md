# 🎯 Live Video QR + Face Verification System

## 🧠 Overview
This project implements a **real-time user authentication system** that combines **QR code scanning** and **facial recognition**.  
It verifies a person’s identity through a live webcam feed by using **DeepFace embeddings** and a **MongoDB database** for secure access validation.

---

## ⚙️ Features
- 📸 Live face capture and embedding extraction using **DeepFace (Facenet)**
- 🔒 Unique QR code generation for every registered user
- 🧩 Real-time face + QR verification with **cosine similarity**
- 🗃️ MongoDB Atlas integration to store user data and logs
- 🎥 Real-time video stream verification using **OpenCV**

---

## 🧩 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Face Recognition | DeepFace (Facenet) |
| QR Code | qrcode (PIL) |
| Video Stream | OpenCV |
| Database | MongoDB Atlas |
| ML Metric | Cosine Similarity |
| Programming Language | Python |

---

## 📂 Folder Structure

live-video-qr-face-verification/
│
├── main.py # Main application file
├── requirements.txt # Dependencies list
├── README.md # Project documentation
├── .gitignore # Ignored files/folders
├── generated_qr/ # Generated QR codes
├── faces_detected/ # Captured face images
└── qr_detected/ # For QR snapshots (optional)

yaml
Copy code

---

## 🧰 Installation

### 1. Clone the Repository
git clone https://github.com/<your-username>/live-video-qr-face-verification.git
cd live-video-qr-face-verification
2. Create a Virtual Environment (optional but recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure MongoDB
Create a free cluster on MongoDB Atlas

Copy your connection string and replace it in main.py:

python
Copy code
MONGO_URI = "your_mongodb_connection_string"
🚀 Usage
Run the main program:

bash
Copy code
python main.py
Menu Options
pgsql
Copy code
1. Register new user (live video)
2. Verify user (live video)
3. Exit
During registration, press C to capture your face.

During verification, hold your QR code in front of the webcam.

Press Q or Esc to exit the video window at any time.

🗃️ MongoDB Collections
Collection	Description
users	Stores user ID, name, QR data, and facial embedding
logs	Stores access attempts with timestamp and verification result

🧩 Working Process
User Registration

Captures face from webcam

Generates Facenet embedding

Creates a unique QR code containing user_id|name

Saves user data in MongoDB

User Verification

Reads QR code from live video

Extracts live face and generates embedding

Compares similarity with stored embedding

If similarity > 0.40 → ✅ Access Granted, else ❌ Denied

Stores verification log in MongoDB

🧠 Example Workflow
Step	Description
1️⃣	Run program and select Register user
2️⃣	Capture face and generate QR code
3️⃣	Hold QR code to camera for verification
4️⃣	System verifies face + QR and grants access
5️⃣	MongoDB logs each attempt

⚡ Future Enhancements
Admin dashboard for user management and logs

Multi-face detection and verification in a single frame

Integration with IoT (door lock, attendance system)

Web app or Streamlit interface for non-technical users

📸 Demo Idea
Add a short GIF or video in the repo later showing:

Face registration

QR generation

Live access verification

Example placeholder:

markdown
Copy code
![Demo GIF](demo/demo.gif)
