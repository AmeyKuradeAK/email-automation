from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains by default

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'markdown' not in request.files or 'csv' not in request.files:
            return jsonify({"error": "Both Markdown and CSV files are required", "status": "error"}), 400

        markdown_file = request.files['markdown']
        csv_file = request.files['csv']

        if markdown_file.filename == '' or csv_file.filename == '':
            return jsonify({"error": "No file selected", "status": "error"}), 400

        markdown_path = os.path.join(app.config['UPLOAD_FOLDER'], markdown_file.filename)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)

        markdown_file.save(markdown_path)
        csv_file.save(csv_path)

        return jsonify({
            "message": "Files uploaded successfully!",
            "status": "success",
            "markdown_file": markdown_path,
            "csv_file": csv_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
