from flask import Flask, request, render_template, send_from_directory, abort

import os
import uuid
import sqlite3
from dotenv import load_dotenv
import openai


# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize DB
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['photo']
        if file:
            img_id = str(uuid.uuid4())
            filename = f"{img_id}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Store in DB
            conn = sqlite3.connect('viewonce.db')
            c = conn.cursor()
            c.execute("INSERT INTO images (id, filename) VALUES (?, ?)", (img_id, filename))
            conn.commit()
            conn.close()

            return f"Link: {request.host_url}view/{img_id}"
        


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
            # Mark as viewed
            c.execute("UPDATE images SET viewed=1 WHERE id=?", (img_id,))
            conn.commit()
            conn.close()

            # Example OpenAI usage: Log message
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"A secure image with ID {img_id} was viewed once. Generate a short log entry."}
                    ]
                )
                print("OpenAI log:", response['choices'][0]['message']['content'])
            except Exception as e:
                print("OpenAI error:", e)

            return render_template('view.html', filename=filename)
    else:
        conn.close()
        abort(404)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    import os
    os.makedirs('uploads', exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    

