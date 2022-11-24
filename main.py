from __future__ import unicode_literals, print_function
from yt_dlp import YoutubeDL
from flask import Flask, render_template, request, send_file, redirect, abort, jsonify
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
from docx2pdf import convert
import time
from pdf2image import convert_from_path, convert_from_bytes
from moviepy.editor import *
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from img2pdf import *
from flask_ipban import IpBan
import stripe
UPLOAD_FOLDER = 'uploads'

DOWNLOAD_FOLDER = 'downloads'


app = Flask(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'png', 'jpg'}
#10.24.189.125
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KOCPZSFoweNIDQpCw8s174zt9sjOjtq8ixnpHbsRRjGduKC5PBU0zQB5ZDnmxDG9ZW5kFnHOwB4oCwFHIgHs2v100XZXSV9K2'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KOCPZSFoweNIDQpj0y9HkUgc0eRhHR7iLXCT83urVJTyRgesCJzBF6s8VAlvEe0DGPE1tIoSX3vsNMETEFg1KfT00sIX6Q43f'


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")  # home page
def home():
    

    return render_template("index.html")

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
    try:
        input = request.form.get("url")  # gets input from the user
        url = YouTube(input).thumbnail_url  # defining thumbnail url
        title = YouTube(input).title  # displays title

    # rendering everything
        return render_template("thumbnail.html", img=url, tit=title)
    except:
        
        error = "Oops something went wrong"
        return render_template("thumbnail.html", tit=error)



@app.route("/video")  # path to download youtube vidoes
def video():

    return render_template("video.html")


@app.route("/video", methods=["POST"])
def video_post():

    if request.form['submit'] == '1080p':
        try:
            
            input = request.form['url']  # gets input from the user
            download_path = YoutubeDL.download([input])
            fname = download_path.split('//')[-1]
            return send_file(fname, as_attachment=True)
        except Exception as e:
            print(e)
            return render_template('video.html', error="Oops something went wrong")

    elif request.form['submit'] == '720p':
        try:
            input = request.form.get("url")  # gets input from the user
            download_path = YouTube(input).streams.get_by_itag(22).download()
            fname = download_path.split('//')[-1]
            return send_file(fname, as_attachment=True)
        except:
            
            render_template('video.html', error="Oops something went wrong")

    elif request.form['submit'] == '360p':
        try:
            input = request.form.get("url")
            download_path = YouTube(input).streams.get_by_itag(18).download()
            fname = download_path.split('//')[-1]
            return send_file(fname, as_attachment=True)
        except:
            return render_template('video.html', error="Oops something went wrong")
                       
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/music", methods=['GET', 'POST'])  # path to lyrics
def music():

    return render_template('music.html')


@app.route("/music_s", methods=['GET', 'POST'])  # path to lyrics
def music_post():
    try:
        
        input = request.form.get("url")  # gets input from the user
        download_path = YouTube(input).streams.get_by_itag(251).download()
        fname = download_path.split('//')[-1]
        return send_file(fname, as_attachment=True)
    except:
        return render_template('music.html', error="Oops something went wrong")


@app.route("/img")  # path to pdf to docx
def pdf2docx():
    return render_template("img.html")


@app.route("/img", methods=["POST"])
def pdf2docx_post():
    if request.method == 'POST':
        img = request.files['img']
        options = request.form['options']

        if img and (options != 'escolha'):
            im = Image.open(img)

            if options == 'png':
                r = im.save("download.png")

                return send_file("download.png", as_attachment=True)
                time.sleep(30)
                os.remove("download.png")
            elif options == 'jpg':
                im = Image.open(img)
                rgb_im = im.convert('RGB')
                rgb_im.save('download.jpg')

                return send_file("download.jpg", as_attachment=True)
                time.sleep(30)
                os.remove("download.jpg")
            elif options == 'ico':
                r = im.save("download.ico")

                return send_file("download.ico", as_attachment=True)
                time.sleep(30)
                os.remove("download.ico")
            elif options == 'bmp':
                im = Image.open(img)
                rgb_im = im.convert('RGB')
                rgb_im.save('download.BMP')

                return send_file("download.BMP", as_attachment=True)
                time.sleep(30)
                os.remove("download.BMP")

            else:
                msg = 'invalid format'
                return render_template('img.html', msg=msg)

            success = "successfully converted"
            return render_template('img.html', success=success)

        msg = 'choose image and format'
        return render_template('img.html', msg=msg)

    return render_template('img.html')

# @app.route("/pdf")  # path to pdf to docx
# def pdf():
#    return render_template('pdf.html')

# @app.route("/pdf", methods=["POST"])
# def pdf_post():
#    f = request.files['pdf']
#    f.save(secure_filename(f.filename))
#    filename = f.filename
#    fuilesnames = secure_filename(f.filename)
#    convert(fuilesnames, "output.pdf", pythoncom.CoInitialize())
#    return send_file("output.pdf", as_attachment=True)
#
#
#    if os.path.exists("output.pdf"):
#        os.remove("output.pdf")
#    else:
#        print("The output file does not exist")
#
#    if os.path.exists(fuiilesnames):
#        os.chmod(fuiilesnames, stat.S_IWRITE)
#        os.remove(fuiilesnames)
#
#    else:
#        print("The file does not exist")


@app.route("/imgc")  # path to img to pdf
def img2pdf():
    return render_template('imgc.html')


@app.route("/imgc", methods=["POST"])
def img2pdf_post():
    try:
        img = request.files['file']
        im = Image.open(img)
        im.convert('RGB').save('compressed.jpg', optimize=True, quality=10)
        return send_file("compressed.jpg", as_attachment=True)
    except:
        return render_template('imgc.html', msg="Something went wrong the accepted formats are png and jpg")


@app.route("/policy")  # path to img to pdf
def policy():
    return render_template('policy.html')


@app.route("/terms")
def terms():
    return render_template('terms.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/mp4")
def mp4():
    return render_template('mp4.html')


@app.route("/mp4", methods=["POST"])
def mp4_post():
    try:
        
        f = request.files.get("file")
        f.save(secure_filename(f.filename))
        filename = f.filename
        fuilesnames = secure_filename(f.filename)
        video = VideoFileClip(fuilesnames)
        video.audio.write_audiofile(fuilesnames + ".mp3")

        return send_file(fuilesnames + ".mp3", as_attachment=True)
    except:
        return render_template('mp4.html', msg="Oops something went wrong")
        
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def login_post():
    try:
        email =  request.form.get['email']
        password = request.form.get['password']
        return render_template('index.html')
        
    except:
        return render_template('login.html', msg='Oops something went wrong')
    
stripe.api_key = "sk_test_51KOCPZSFoweNIDQpj0y9HkUgc0eRhHR7iLXCT83urVJTyRgesCJzBF6s8VAlvEe0DGPE1tIoSX3vsNMETEFg1KfT00sIX6Q43f"

    

if __name__ == "__main__":
    port =  3000 #int(os.environ.get("PORT")) or 3000
    app.run(debug=True, host='0.0.0.0',port=port,threaded=True)
