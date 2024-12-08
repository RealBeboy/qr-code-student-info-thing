import qrcode
import sqlite3

def generate_qr_code():
    """Generates a QR Code, stores data in the database, and saves it as an image."""
    print("Enter the following details to generate a QR Code:")
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    lrn = input("LRN #: ").strip()
    gender = input("Gender: ").strip()

    # Connect to the database
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            lrn TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            photo TEXT
        )
    ''')
    
    # Format the QR code data
    qr_data = f"Name: {name}\nAge: {age}\nLRN#: {lrn}\nGender: {gender}"
    qr_filename = f"{lrn}_qr.png"

    try:
        # Insert data into the database
        cursor.execute('''
            INSERT INTO students (lrn, name, age, gender, photo)
            VALUES (?, ?, ?, ?, ?)
        ''', (lrn, name, age, gender, f"{lrn}_photo.jpg"))
        conn.commit()

        # Generate and save the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')
        qr_img.save(qr_filename)
        print(f"QR Code generated and saved as {qr_filename}. Student added to the database.")
    except sqlite3.IntegrityError:
        print("A student with this LRN already exists in the database.")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_qr_code()