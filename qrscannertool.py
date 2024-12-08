import cv2
from pyzbar.pyzbar import decode
import requests

def parse_qr_data(qr_data):
    """Parses the QR code data into a dictionary."""
    try:
        lines = qr_data.strip().split('\n')
        return {
            'name': lines[0].split(': ')[1],
            'age': int(lines[1].split(': ')[1]),
            'lrn': lines[2].split(': ')[1],
            'gender': lines[3].split(': ')[1],
        }
    except (IndexError, ValueError) as e:
        print(f"Error parsing QR Code: {e}")
        return None

def update_student_info(student_info):
    """Sends the student data to the Flask app for update."""
    try:
        response = requests.post('http://127.0.0.1:5000/update_student_info', json=student_info)
        if response.status_code == 200:
            print("Student information updated successfully.")
        else:
            print("Failed to update student information.")
    except Exception as e:
        print(f"Error sending data to Flask: {e}")

def scan_qr_code():
    """Scans QR codes continuously and updates the website with the data."""
    cap = cv2.VideoCapture(0)
    print("Point the camera to the QR Code. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            break

        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")
            student_info = parse_qr_data(qr_data)
            if student_info:
                update_student_info(student_info)
                print("Scanned and updated website successfully!")

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()