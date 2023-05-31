# Code Documentation - Face Detection and Image Capture

This Python script utilizes OpenCV to perform face detection using Haar cascades and captures images when a face is detected for a specified duration. The captured image is then sent as an email attachment using SMTP.

## Requirements

To run this code, the following packages need to be installed:

- `cv2` (OpenCV)
- `time`
- `os`
- `smtplib`
- `email`

Make sure these packages are installed in your Python environment.

## Configuration

Before running the script, you need to configure the following variables:

- `SAVE_DIR`: The directory where captured images will be saved. If the directory doesn't exist, it will be created.
- `SMTP_SERVER`: The SMTP server address.
- `SMTP_PORT`: The SMTP server port.
- `SENDER_EMAIL`: The email address of the sender.
- `SENDER_PASSWORD`: The password for the sender's email address.
- `RECIPIENT_EMAIL`: The email address of the recipient.

Make sure to update these variables with the appropriate values before running the code.

## Functionality

### `detect_faces(frame)`

This function takes a frame (image) as input and returns `True` if at least one face is detected, and `False` otherwise. It uses the Haar cascade classifier for face detection.

### `capture_image(face_duration)`

This function opens the camera, reads frames from the camera, and displays them. It continuously checks for faces in the frames using `detect_faces()`. If a face is detected, it starts a timer (`face_start_time`) and updates the `face_present` variable accordingly. If a face is not detected, it resets the `face_present` variable.

If a face is detected for more than 10 seconds (controlled by `face_duration`), it captures the current frame as an image, saves it to the specified `SAVE_DIR` directory with a timestamped filename, and then sends an email with the captured image as an attachment using `send_email_with_attachment()`.

The function exits if 'q' is pressed or when the image is captured and sent.

### `send_email_with_attachment(image_path)`

This function creates an email message with the captured image as an attachment. It sets the sender and recipient email addresses, the subject, and attaches the image to the email. It connects to the SMTP server using the provided server address and port, and authenticates using the sender's email address and password. Finally, it sends the email message.

## Usage

To use the script, call the `capture_image()` function with the desired face duration (in seconds) as the argument. The script will open the camera, display the frames, detect faces, and capture an image if a face is detected for the specified duration. The captured image will be saved to the specified directory and sent as an email attachment.

Example usage:

```python
python CamCap.py
```

**Note:** Make sure to update the configuration variables and have a camera connected to the system before running the script.