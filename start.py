import os
import shutil
from flask import Flask, render_template, request, send_file
import webbrowser
import time
import threading

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

for folder in [UPLOAD_FOLDER, RESULT_FOLDER, DOWNLOADS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def remove_duplicates(file1, file2):
    """Remove duplicates by combining two files."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.read().splitlines()
        lines2 = f2.read().splitlines()
      
    all_lines = lines1 + lines2
    unique_lines = sorted(set(all_lines))

    return unique_lines

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        path1 = os.path.join(UPLOAD_FOLDER, 'file1.txt')
        path2 = os.path.join(UPLOAD_FOLDER, 'file2.txt')

        file1.save(path1)
        file2.save(path2)

        unique_lines = remove_duplicates(path1, path2)

        result_path = os.path.join(RESULT_FOLDER, 'unique_combined.txt')
        with open(result_path, 'w') as result_file:
            result_file.write('\n'.join(unique_lines))

        download_path = os.path.join(DOWNLOADS_FOLDER, 'unique_combined.txt')
        shutil.copy(result_path, download_path)

        return send_file(result_path, as_attachment=True)

    return render_template('index.html')

def open_browser():
    """Open the web browser with a delay to allow the server to start."""
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5001/')

if __name__ == '__main__':
    server_thread = threading.Thread(target=lambda: app.run(debug=True, port=5001, use_reloader=False)) 
    server_thread.start()

    open_browser()
