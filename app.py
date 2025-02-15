from flask import Flask, render_template, request, send_from_directory, redirect, url_for,jsonify
import yt_dlp
import os

app = Flask(__name__)

# Configure download and cache directories
DOWNLOAD_FOLDER = os.path.join(app.instance_path, 'downloads')
CACHE_FOLDER = os.path.join(app.instance_path, 'yt-dlp-cache')
COOKIE_FILE_PATH = 'youtube.com_cookies.txt'  # Update for Render!
COOKIE_FILE_PATH2 = 'instagram.com_cookies.txt'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(CACHE_FOLDER, exist_ok=True)


app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER



@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")  # Ana sayfa (Platform Seçme)



@app.route("/youtube", methods=["GET", "POST"])
def youtube():
    if request.method == "POST":
        url = request.form.get("url")

        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
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
            return render_template("youtube.html", error=error_message)

    return render_template("youtube.html")



@app.route("/instagram", methods=["GET", "POST"])
def instagram():
    if request.method == "POST":
        url = request.form.get("url")

        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Similar format selection
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'), # Output filename
                # You likely don't need 'noplaylist' for Instagram
                'cachedir': CACHE_FOLDER,
                'cookiefile': COOKIE_FILE_PATH2 #  Important: Use cookies if necessary for Instagram
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                filename = get_downloaded_filename(ydl, url)

                if filename:
                    return redirect(url_for('download_file', filename=filename)) # Redirect to download
                else:
                    raise ValueError("Could not determine downloaded filename.")

        except Exception as e:
            print(f"Instagram download error: {e}")
            error_message = f"Instagram download error: {e}"
            return render_template("instagram.html", error=error_message)  # Render Instagram error template

    return render_template("instagram.html") # Render Instagram input form




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
