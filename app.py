from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io
import os  # Ensure you import os to access environment variables
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "image" not in request.files:
            return "No image uploaded", 400

        image_file = request.files["image"]
        image = Image.open(image_file)

        output = remove(image)

        img_io = io.BytesIO()
        output.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    # Modify this line to use the dynamic port
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
