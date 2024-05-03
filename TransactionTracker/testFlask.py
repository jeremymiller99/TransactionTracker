from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join('uploads', filename)
            file.save(save_path)
            # Process the file here
            return render_template('file_uploaded.html', filename=filename)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
