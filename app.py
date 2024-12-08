from flask import Flask, render_template_string, send_from_directory, request, jsonify
import os

app = Flask(__name__)

# Define the path for static files (student photos)
PHOTO_FOLDER = 'student_photos'

# Store student information in a variable
student_info = {
    "name": "",
    "age": "",
    "lrn": "",
    "gender": "",
    "photo": "",
}

@app.route("/")
def home():
    """Serves the dynamic student information page with auto-refresh."""
    global student_info
    if student_info["photo"]:
        # Make sure the student photo exists before rendering the page
        photo_url = f"/student_photos/{student_info['photo']}"
    else:
        photo_url = None

    # Define the HTML template with placeholders for student information
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Information</title>
    <style>
        /* Global Styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e3f2fd; /* Light Blue */
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }

        h1 {
            font-size: 40px;
            color: #1976d2; /* Blue */
            margin-bottom: 20px;
        }

        /* School Logo */
        .logo-container {
            margin-bottom: 20px;
        }

        .logo-container img {
            width: 120px;
            height: auto;
            object-fit: contain;
        }

        /* Card Style for Information */
        .info-card {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 350px;
            text-align: center;
            margin-top: 20px;
            transition: all 0.3s ease;
        }

        .info-card:hover {
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        /* Photo Styling */
        .photo-container {
            width: 160px;
            height: 160px;
            margin: 0 auto;
            border-radius: 50%;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .photo-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* Text Styles */
        p {
            font-size: 20px; /* Larger text */
            line-height: 1.6;
            margin: 15px 0;
            color: #333;
        }

        strong {
            color: #1976d2; /* Blue */
        }

        /* Error Message */
        .no-photo {
            font-size: 18px;
            color: #f44336; /* Red */
        }

    </style>
    <script>
        // Auto-refresh every 500 milliseconds
        setInterval(function() {
            window.location.reload();
        }, 500);
    </script>
</head>
<body>

    <!-- School Logo -->
    <div class="logo-container">
        <img src="logo.png" alt="School Logo"> <!-- Replace with your logo path -->
    </div>

    <h1>Student Information</h1>

    <div class="info-card">
        <div class="photo-container">
            {% if photo_url %}
                <img src="{{ photo_url }}" alt="Student Photo">
            {% else %}
                <div class="no-photo">No photo available</div>
            {% endif %}
        </div>

        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Age:</strong> {{ age }}</p>
        <p><strong>LRN:</strong> {{ lrn }}</p>
        <p><strong>Gender:</strong> {{ gender }}</p>
    </div>

</body>
</html>


    """
    # Pass student information into the template
    return render_template_string(html_template, 
                                  photo_url=photo_url, 
                                  name=student_info["name"], 
                                  age=student_info["age"], 
                                  lrn=student_info["lrn"], 
                                  gender=student_info["gender"])

@app.route("/student_photos/<filename>")
def serve_photo(filename):
    """Serves the student's photo from the static folder."""
    return send_from_directory(PHOTO_FOLDER, filename)

@app.route("/update_student_info", methods=["POST"])
def update_student_info():
    """Updates student information from the QR scan."""
    global student_info
    student_info = {
        "name": request.json.get("name", ""),
        "age": request.json.get("age", ""),
        "lrn": request.json.get("lrn", ""),
        "gender": request.json.get("gender", ""),
        "photo": f"{request.json.get('lrn')}.jpg"  # Dynamically setting the photo path based on LRN
    }
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)