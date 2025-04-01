from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import os
import uuid
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['photo']
        if file:
            img_id = str(uuid.uuid4())
            filename = f"{img_id}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = sqlite3.connect('viewonce.db')
            c = conn.cursor()
            c.execute("INSERT INTO images (id, filename) VALUES (?, ?)", (img_id, filename))
            conn.commit()
            conn.close()

            link = request.host_url + "view/" + img_id
            return render_template("upload_success.html", link=link)

    return render_template('upload.html')

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
            return "This image has already been viewed."
        else:
            c.execute("UPDATE images SET viewed=1 WHERE id=?", (img_id,))
            conn.commit()
            conn.close()
            return render_template('view.html', filename=filename)
    else:
        conn.close()
        abort(404)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
