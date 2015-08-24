from flask import Flask
from flask import render_template

app = Flask(__name__)

TEMP_PATH = "/tmp/tiles"
TILES_PATH = "/var/www/tiles"


@app.route('/')
def upload_page():
	return render_template("uploader.html")

@app.route("/upload")
def upload():
	pass







if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0")

