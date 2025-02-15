from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

# Configure upload and download directories
UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')
DOWNLOAD_FOLDER = os.path.join(app.instance_path, 'downloads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()  # You can change this to get different resolutions/formats
            filename = stream.download(output_path=app.config['DOWNLOAD_FOLDER'])
            return redirect(url_for('download_file', filename=os.path.basename(filename)))
        except Exception as e:
            print(e) # Log the error for debugging
            error_message = "Invalid YouTube URL or download error."
            return render_template("index.html", error=error_message)

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
