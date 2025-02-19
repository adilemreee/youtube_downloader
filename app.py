from flask import Flask, render_template, request, Response
import yt_dlp
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/youtube", methods=["GET", "POST"])
def youtube():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'noplaylist': True,
                'http_headers': {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.youtube.com/'
}

            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                stream_url = info_dict.get('url', None)
                title = info_dict.get('title', 'video')

                if stream_url:
                    return render_template("stream.html", stream_url=stream_url, platform="YouTube", title=title)

                else:
                    raise ValueError("Could not retrieve stream URL.")

        except Exception as e:
            print(f"Error: {e}")
            error_message = f"Error: {e}"
            return render_template("youtube.html", error=error_message)

    return render_template("youtube.html")


@app.route("/instagram", methods=["GET", "POST"])
def instagram():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'noplaylist': True,
                'http_headers': {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.youtube.com/'
}

            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                stream_url = info_dict.get('url', None)
                title = info_dict.get('title', 'video')

                if stream_url:
                    return render_template("stream.html", stream_url=stream_url, platform="Instagram", title=title)

                else:
                    raise ValueError("Could not retrieve stream URL.")

        except Exception as e:
            print(f"Instagram Error: {e}")
            error_message = f"Instagram Error: {e}"
            return render_template("instagram.html", error=error_message)

    return render_template("instagram.html")


@app.route("/download")
def download():
    video_url = request.args.get("url")
    filename = request.args.get("filename", "video.mp4")

    if not video_url:
        return "Invalid video URL", 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Bazı videolar için gerekli olabilir
        response = requests.get(video_url, stream=True, headers=headers)

        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers["Content-Type"],
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        print(f"Download Error: {e}")
        return "Error while downloading", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
