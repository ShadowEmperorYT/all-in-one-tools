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
from docx2pdf import convert
import time
from pdf2image import convert_from_path, convert_from_bytes
#import pythoncom


UPLOAD_FOLDER = 'uploads'

DOWNLOAD_FOLDER = 'downloads'


app = Flask(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx','png','jpg'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


    
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

@app.route("/img")  # path to pdf to docx
def pdf2docx():
    return render_template("img.html")

@app.route("/img", methods=["POST"])
def pdf2docx_post():
    if request.method == 'POST':
        img = request.files['img']
        options = request.form['options']
        
        if  img and (options != 'escolha'):
            im = Image.open(img)
            
            if options == 'png':
                r = im.save("download.png")
                time.sleep(10)
                return send_file("download.png", as_attachment=True)
                time.sleep(30)
                os.remove("download.png")
            elif options == 'jpg':
                im = Image.open(img)
                rgb_im = im.convert('RGB')
                rgb_im.save('download.jpg')     
                time.sleep(10)
                return send_file("download.jpg", as_attachment=True)
                time.sleep(30)
                os.remove("download.jpg")
            elif options == 'ico':
                r = im.save("download.ico")
                time.sleep(10)
                return send_file("download.ico", as_attachment=True)
                time.sleep(30)
                os.remove("download.ico")
            elif options == 'bmp':
                im = Image.open(img)
                rgb_im = im.convert('RGB')
                rgb_im.save('download.BMP')
                time.sleep(10)
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

#@app.route("/pdf")  # path to pdf to docx
#def pdf():
#    return render_template('pdf.html')

#@app.route("/pdf", methods=["POST"])
#def pdf_post():
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
        

    
        
    
    
    
    
    
        
    
    
            
    
        
    
    
if __name__ == "__main__":
    app.run(debug=True)
