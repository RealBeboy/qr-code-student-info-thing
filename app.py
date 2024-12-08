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
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 20px;
            }
            img {
                width: 200px;
                height: 200px;
                border-radius: 50%;
            }
        </style>
        <script>
            // Auto-refresh every 5 seconds
            setInterval(function() {
                window.location.reload();
            }, 500);
        </script>
    </head>
    <body>
        <h1>Student Information</h1>
        {% if photo_url %}
            <img src="{{ photo_url }}" alt="Student Photo">
        {% else %}
            <p>No photo available</p>
        {% endif %}
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Age:</strong> {{ age }}</p>
        <p><strong>LRN:</strong> {{ lrn }}</p>
        <p><strong>Gender:</strong> {{ gender }}</p>
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