from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import os
import uuid
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Database setup ---
def init_db():
    conn = sqlite3.connect('viewonce.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id TEXT PRIMARY KEY,
            filename TEXT,
            viewed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Utility: Check allowed file extensions ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Route: Upload Page ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            img_id = str(uuid.uuid4())
            filename = secure_filename(f"{img_id}.{ext}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Save record to database
            conn = sqlite3.connect('viewonce.db')
            c = conn.cursor()
            c.execute("INSERT INTO images (id, filename) VALUES (?, ?)", (img_id, filename))
            conn.commit()
            conn.close()

            link = url_for('view_image', img_id=img_id, _external=True)
            return render_template("upload_success.html", link=link)
        else:
            return "Invalid file type. Only JPG, JPEG, PNG, and GIF are allowed.", 400

    return render_template('upload.html')

# --- Route: View Image ---
@app.route('/view/<img_id>')
def view_image(img_id):
    conn = sqlite3.connect('viewonce.db')
    c = conn.cursor()
    c.execute("SELECT filename, viewed FROM images WHERE id=?", (img_id,))
    row = c.fetchone()

    if row:
        filename, viewed = row
        if viewed:
            conn.close()
            return "This image has already been viewed or expired."
        else:
            c.execute("UPDATE images SET viewed=1 WHERE id=?", (img_id,))
            conn.commit()
            conn.close()
            return render_template('view.html', filename=filename)
    else:
        conn.close()
        abort(404)

# --- Route: Serve uploaded image ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/test-sound')
def test_sound():
    return '''
    <audio controls autoplay>
      <source src="/static/siren.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    '''

# --- Run the Flask App ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)