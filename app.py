import os
import sys
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

# Configure Flask app with environment variables
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key_for_local_dev')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')

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
    # Explicitly get port from environment
    port = int(os.environ.get("PORT", 5000))
    
    # Print port for debugging
    print(f"Starting server on port {port}", file=sys.stderr)
    
    # Bind to 0.0.0.0 for all interfaces
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
