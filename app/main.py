from __future__ import unicode_literals
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
from mcstatus import MinecraftServer
from pytube import YouTube
from PyLyrics import *
from PIL import Image
import os
from datetime import datetime
import youtube_dl
from tube_dl import Youtube
from pydub import AudioSegment


UPLOAD_FOLDER = 'uploads'

DOWNLOAD_FOLDER = 'downloads'


app = Flask(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route("/")  # home page
def home():
    return render_template("index.html")  # renders index.html


@app.route("/stats")  # minecraft status page route
def stats():
    return render_template("status.html")  # renders the minecraft status page


# post methond of mc status to get the information from the use
@app.route("/stats", methods=["POST"])
def stats_post():
    try:
        input = request.form["ip"]  # users input
        # searches for the minecraft server ip
        server = MinecraftServer.lookup(input)
        status = server.status()  # fetches the status
        # displays the minecraft server status in html
        return render_template("status.html", players=status.players.online, mplayers=status.players.max, verion=status.version.name, motd=status.description, favicon=status.favicon)

    except:  # in case of any error
        error = "Invalid ip or server didnt responded"
        return render_template("status.html", players=error, mplayers=error, verion=error, motd=error, favicon=error)


@app.route("/thumbnail")  # path to thumbnail downloader
def thumbnail():
    return render_template("thumbnail.html")  # renders thumbnails.html


# post method to get the data form the user
@app.route("/thumbnail", methods=["POST"])
def thumbnail_post():
  #  try:

    input = request.form.get("url")  # gets input from the user
    url = YouTube(input).thumbnail_url  # defining thumbnail url
    title = YouTube(input).title  # displays title

    # rendering everything
    return render_template("thumbnail.html", img=url, tit=title)

    # except: #using except and try in case of any error
 #   error = "Oops something went wrong"
  #  return render_template("thumbnail.html", tit=error)


@app.route("/video")  # path to download youtube vidoes
def video():

    return render_template("video.html")


@app.route("/video", methods=["POST"])
def video_post():

    if request.form['submit'] == '1080p':
        input = request.form.get("url")  # gets input from the user
        download_path = YouTube(input).streams.get_by_itag(137).download()
        fname = download_path.split('//')[-1]
        return send_file(fname, as_attachment=True)

    if request.form['submit'] == '720p':
        input = request.form.get("url")  # gets input from the user
        download_path = YouTube(input).streams.get_by_itag(22).download()
        fname = download_path.split('//')[-1]
        return send_file(fname, as_attachment=True)

    if request.form['submit'] == '360p':
        input = request.form.get("url")
        download_path = YouTube(input).streams.get_by_itag(18).download()
        fname = download_path.split('//')[-1]
        return send_file(fname, as_attachment=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/music", methods=['GET', 'POST'])  # path to lyrics
def music():

    return render_template('music.html')


@app.route("/music_s", methods=['GET', 'POST'])  # path to lyrics
def music_post():
    input = request.form.get("url")  # gets input from the user
    download_path = YouTube(input).streams.get_by_itag(251).download()
    fname = download_path.split('//')[-1]
    return send_file(fname, as_attachment=True)

    


if __name__ == "__main__":
    app.run(debug=True)
