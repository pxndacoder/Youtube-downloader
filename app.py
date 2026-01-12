from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audio", methods=["GET", "POST"])
def audio():
    filename = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['title']}.mp3"

        except Exception as e:
            error = str(e)

    return render_template("audio.html", filename=filename, error=error)


@app.route("/video", methods=["GET", "POST"])
def video():
    filename = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        try:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['title']}.mp4"

        except Exception as e:
            error = str(e)

    return render_template("video.html", filename=filename, error=error)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
