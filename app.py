from flask import Flask, url_for, request, redirect
from flask import render_template
from werkzeug import secure_filename
import os
import subprocess
import json

UPLOAD_FOLDER = "/tmp/tiles"
TILES_PATH = "/var/www/tiles"
BASE_URL = "http://tiles.openhistorymap.org/"

MAX_ZOOM = 2
MIN_ZOOM = 1

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template("index.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		ff = request.files['file']
		if ff :
			filename = secure_filename(ff.filename)
			the_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			the_folder = os.path.join(TILES_PATH, filename)
			ff.save(the_file)
			subprocess.call("gdal2tiles.py -w none %s %s" % (the_file, the_folder), shell=True)
			miz = 1000
			maz = 0
			for z in os.listdir(the_folder):
				try:
					z = int(z)
					miz = min(z,miz)
					maz = max(z,maz)
				except:
					print z
			subprocess.call("gdal2tiles.py -w none -e -z %s-%s %s %s" % (miz-MIN_ZOOM, maz+MAX_ZOOM, the_file, the_folder), shell=True)

			return redirect(url_for('index'))
	else:
		return render_template("uploader.html")


@app.route("/list")
def list():
	out = {}
	l = os.listdir(TILES_PATH)
	for u in l:
		f = os.path.join(TILES_PATH, u)
		with open(os.path.join(f,"tilemapresource.xml"), "rb") as x:
			for x in x.readlines():
				if "BoundingBox" in x:
					bb = x.split("\"")
					bb = [bb[1],bb[3],bb[5],bb[7]]
		miz = 1000
		maz = 0
		for z in os.listdir(f):
			try:
				z = int(z)
				miz = min(z,miz)
				maz = max(z,maz)
			except:
				print z
		out[u] = {"url":BASE_URL+u, "minzoom": miz, "maxzoom":maz, "bbox":bb}
	
	return json.dumps(out)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
