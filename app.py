from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecret"
UPLOAD_FOLDER = "static/uploads"
DATA_FILE = "data.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 读取已有数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# 保存数据
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ------------------ 路由 ------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("image")
        seed = request.form.get("seed")
        publickey = request.form.get("publickey")

        if not file or not seed or not publickey:
            flash("请填写所有字段", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 保存到 data.json
        data = load_data()
        data.append({
            "filename": filename,
            "seed": seed,
            "publickey": publickey
        })
        save_data(data)

        flash("上传成功", "success")
        return redirect(url_for("upload"))

    return render_template("upload.html")

@app.route("/find")
def find():
    data = load_data()
    return render_template("find.html", data=data)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/download')
def download():
    # 从 static 文件夹里返回 exe 文件
    return send_from_directory('static', 'myprogram.exe', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)