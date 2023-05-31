import cv2
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')


SAVE_DIR = 'captured_images'

SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@example.com'
SENDER_PASSWORD = 'your_password'
RECIPIENT_EMAIL = 'recipient@example.com'


# Create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

    
def detect_faces(frame):
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Return True if at least one face is detected, False otherwise
    return len(faces) > 0


def capture_image(face_duration):
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Failed to open the camera.")
        return

    # Read and display frames from the camera
    while True:
        ret, frame = cap.read()

        # Check if frame reading was successful
        if not ret:
            print("Failed to read frame from the camera.")
            break

        # Display the frame
        cv2.imshow("Camera", frame)
        
        if detect_faces(frame):
            # If face is already present, update the face duration
            if face_present:
                face_duration = time.time() - face_start_time
            # If face is newly detected, update face_present and face_start_time
            else:
                face_present = True
                face_start_time = time.time()
        else:
            # If face is not detected, reset face_present and face_start_time
            face_present = False
            face_start_time = time.time()

        # Capture an image if a face has been detected for more than 10 seconds
        if face_present and face_duration > 10:
            # Save the frame as an image
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            image_filename = f"image_{timestamp}.jpg"
            image_path = os.path.join(SAVE_DIR, image_filename)
            cv2.imwrite(image_path, frame)
            print(f"Image captured and saved: {image_path}")

            send_email_with_attachment(image_path)
            print("Email sent with the captured image.")

            
            break


        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()



def send_email_with_attachment(image_path):
    # Create a multipart message object
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Captured Image'

    # Attach the image to the email
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image_mime = MIMEImage(image_data, name=os.path.basename(image_path))
    msg.attach(image_mime)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)



capture_image(0)