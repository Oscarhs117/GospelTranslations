import os
import tempfile
from flask import Flask, request, jsonify
import dropbox
from utils.extract_text import extract_text

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def handle_file():
    data = request.get_json()
    file_path = data.get("path_display")

    if not file_path:
        return jsonify({"error": "Falta 'path_display'"}), 400

    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        _, res = dbx.files_download(file_path)

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(res.content)
            tmp_path = tmp.name

        extracted_text = extract_text(tmp_path)
        os.remove(tmp_path)

        return jsonify({
            "text": extracted_text
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
