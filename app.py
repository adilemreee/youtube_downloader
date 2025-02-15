from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# Configure download and cache directories
DOWNLOAD_FOLDER = os.path.join(app.instance_path, 'downloads')
CACHE_FOLDER = os.path.join(app.instance_path, 'yt-dlp-cache')
COOKIE_FILE_PATH = '/mnt/disks/youtube-cookies/youtube.com_cookies.txt'  # Update for Render!

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(CACHE_FOLDER, exist_ok=True)


app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'noplaylist': True,
                'cachedir': CACHE_FOLDER,
                'cookiefile': COOKIE_FILE_PATH  # Use the cookies
            }


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                filename = get_downloaded_filename(ydl, url)
                if filename:
                    return redirect(url_for('download_file', filename=filename))
                else:
                    raise ValueError("Could not determine downloaded filename.")

        except Exception as e:
            print(f"Download error: {e}")
            error_message = f"Download error: {e}"
            return render_template("index.html", error=error_message)

    return render_template("index.html")

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']}")


def get_downloaded_filename(ydl, url):
    try:
        info_dict = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info_dict)
        return os.path.basename(filename)
    except Exception as e:
        print(f"Error retrieving filename: {e}")
        return None


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
