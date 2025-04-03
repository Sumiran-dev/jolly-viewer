# 🚨 Jolly Viewer – The One-Time Secure Photo Viewer

Welcome to **Jolly Viewer** – a playful yet security-conscious web app that lets you upload and share an image that can **only be viewed once**.  
Think **Snapchat meets Mission Impossible**: the image self-destructs, detects screenshots, and blares sirens for sneaky behavior. Yes, really.

---

## 🔐 What is Jolly Viewer?

**Jolly Viewer** is a Flask-based web app designed to securely share images that can be viewed *once and only once*. Whether it's sensitive information or a funny prank, this app ensures your image doesn’t stick around for long. 

It uses a mix of front-end JavaScript tricks, timed expirations, and detection techniques to discourage screen captures and unauthorized reuse.

---

## ✅ Core Features

- 🔗 One-time access per image  
- 📋 Copy link button on upload success  
- ⏳ Auto-expire after **1 minute**  
- 🔁 Auto-close tab after **2 minutes**  
- 🛡️ Detects PrintScreen key for screenshots  
- 📱 Mobile-aware – triggers siren on tab blur  
- 🚨 Police siren + flashing red/blue light on screenshot attempts  
- ⚡ Fake camera flash effect  
- 🔒 Watermark: *"Jolly Viewer – One Time Only"*  
- 🔙 Redirects to upload page after timeout  

---

## 🧪 How It Works

1. Upload a photo  
2. Get a secret, one-time-view link  
3. Share it (or view it yourself)  
4. Once opened, the image disappears forever  

Behind the scenes:  
The app stores unique image IDs in an SQLite database. Once the image is viewed, it's marked as used and won’t open again.

---

## 🛠 Tech Stack

- Python 3 + Flask  
- SQLite for lightweight tracking  
- HTML, CSS, and JavaScript for front-end wizardry  
- Can be hosted on Render, Replit, or GitHub Pages

---

## 📁 Project Structure

```
├── app.py                   # Main Flask app
├── viewonce.db              # SQLite DB for view tracking
├── uploads/                 # Temp image store (gitignored)
└── templates/
    ├── upload.html
    ├── upload_success.html
    └── view.html
```

---

## ⚙️ Getting Started

```bash
git clone https://github.com/Sumiran-dev/jolly-viewer.git
cd jolly-viewer
pip install -r requirements.txt
python app.py
```

Then open https://jolly-viewer.onrender.com in your browser and give it a spin!

---

## 🤖 Final Thoughts

While it’s not bulletproof (someone *can* still film their screen), **Jolly Viewer** is a creative dive into making content *feel* secure — and fun.  
It’s great for teaching UX around security, surprising friends, or experimenting with front-end protection.

---

It’s perfect for:
- 💬 Pranks with friends
- 🛡️ One-time secure info sharing
- 🎓 Learning about security UX

---

## 🧑‍💻 Author

Made with 💡 curiosity and ☕ caffeine by **Sumiran**  
Feel free to ⭐ this repo if you liked it!

