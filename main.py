# ------------------------
# Live Video QR + Face Verification System with MongoDB
# ------------------------
# pip install deepface opencv-python numpy qrcode[pil] pymongo

import os
import cv2
import qrcode
import numpy as np
from deepface import DeepFace
from datetime import datetime
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
# ------------------------
# Setup folders
# ------------------------
os.makedirs("generated_qr", exist_ok=True)
os.makedirs("faces_detected", exist_ok=True)
os.makedirs("qr_detected", exist_ok=True)

# ------------------------
# MongoDB Setup
# ------------------------
MONGO_URI = "mongodb+srv://saisivaneeli_db_user:1234567890@cluster0.qxs8ddr.mongodb.net/"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['security_system']
users_col = db['users']
logs_col = db['logs']

# ------------------------
# Helper to draw text on frame AND print to console
# ------------------------
def show_and_print(frame, text, org=(50,50), font=cv2.FONT_HERSHEY_SIMPLEX,
                   font_scale=1.0, color=(0,255,0), thickness=2):
    # print to console
    print(text)
    # safe draw if frame is available
    if frame is not None:
        cv2.putText(frame, text, org, font, font_scale, color, thickness)

# ------------------------
# Cosine similarity function
# ------------------------
# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ------------------------
# Register new user (live video)
# ------------------------
def register_user_live():
    name = input("Enter full name: ")
    user_id = input("Enter unique user ID (e.g., EMP003): ")

    if users_col.find_one({"user_id": user_id}):
        print(f"⚠️ User {user_id} already exists. Registration skipped!")
        return

    cap = cv2.VideoCapture(0)
    print("📸 Press 'C' to capture your face for registration.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Capture Face - Press C", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') or key == ord('C'):
            img = frame.copy()
            filename = f"faces_detected/{user_id}_{datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(filename, img)
            print(f"[INFO] Face captured and saved at {filename}")
            break
        elif key == ord('q') or key == 27:
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    # Generate face embedding using DeepFace
    try:
        embedding = DeepFace.represent(img_path=filename, model_name="Facenet", enforce_detection=True)[0]["embedding"]
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return

    # Generate QR code
    qr_data = f"{user_id}|{name}"
    qr_img = qrcode.make(qr_data)
    qr_path = f"generated_qr/{user_id}.png"
    qr_img.save(qr_path)

    # Save user to MongoDB
    users_col.insert_one({
        "user_id": user_id,
        "name": name,
        "qr_data": qr_data,
        "face_embedding": embedding
    })

    print(f"✅ User {name} (ID: {user_id}) registered successfully!")
    print(f"[INFO] QR code saved at {qr_path}")

# ------------------------
# Verify live video (face + QR)
# ------------------------


import cv2
import numpy as np
from deepface import DeepFace
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

def verify_live():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    detector = cv2.QRCodeDetector()

    print("🚁 Drone Mode: Detecting QR + Face...")

    consecutive_matches = 0
    threshold_frames = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Enhance QR detection
        processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.medianBlur(processed, 3)

        # Detect QR
        qr_data, bbox, _ = detector.detectAndDecode(processed)

        if qr_data:
            qr_user_id = qr_data.split("|")[0]
            user = users_col.find_one({"user_id": qr_user_id})

            if user:
                try:
                    # Face detection using RetinaFace
                    faces = DeepFace.extract_faces(
                        img_path=frame,
                        detector_backend="retinaface"
                    )

                    if len(faces) > 0:
                        face_img = faces[0]["face"]

                        # Ensure correct color format
                        if len(face_img.shape) == 2:
                            face_img = cv2.cvtColor(face_img, cv2.COLOR_GRAY2RGB)
                        elif face_img.shape[2] == 4:
                            face_img = face_img[:, :, :3]

                        # Resize for consistency
                        face_img = cv2.resize(face_img, (160, 160))

                        # Generate embedding (NO FACE DETECTION AGAIN)
                        embedding_new = DeepFace.represent(
                            img_path=face_img,
                            model_name="Facenet",
                            enforce_detection=False
                        )[0]["embedding"]

                        stored_emb = np.array(user["face_embedding"])
                        similarity = cosine_similarity([stored_emb], [embedding_new])[0][0]

                        if similarity > 0.40:
                            consecutive_matches += 1
                            show_and_print(frame, f"Matching... {consecutive_matches}/{threshold_frames}",
                                           org=(50,100), color=(255,255,0), thickness=2)
                            
                            if consecutive_matches >= threshold_frames:
                                show_and_print(frame, f"ACCESS GRANTED: {user['name']}", org=(50,50),
                                               color=(0,255,0), thickness=3)
                                logs_col.insert_one({
                                    "user_id": qr_user_id,
                                    "timestamp": str(datetime.now()),
                                    "result": "ACCESS_GRANTED"
                                })
                        else:
                            consecutive_matches = 0
                            show_and_print(frame, "ACCESS DENIED", org=(50,50),
                                           color=(0,0,255), thickness=3)

                    else:
                        show_and_print(frame, "FACE NOT FOUND", org=(50,80),
                                       color=(0,0,255), thickness=2)

                except Exception as e:
                    print("Face processing error:", e)

        # Draw QR bounding box
        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox[0])):
                cv2.line(frame,
                         tuple(bbox[0][i]),
                         tuple(bbox[0][(i + 1) % len(bbox[0])]),
                         (255, 0, 0), 3)

        cv2.imshow("Drone Verification", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'), 27]:
            break

    cap.release()
    cv2.destroyAllWindows()


# ------------------------
# Main system
# ------------------------
def main_system():
    while True:
        print("\n===== LIVE QR + FACE SECURITY SYSTEM =====")
        print("1. Register new user (live video)")
        print("2. Verify user (live video)")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ")
        if choice == "1":
            register_user_live()
        elif choice == "2":
            verify_live()
        elif choice == "3":
            print("Exiting system...")
            break
        else:
            print("Invalid input. Try again.")

# ------------------------
# Run system
# ------------------------
if __name__ == "__main__":
    main_system()
