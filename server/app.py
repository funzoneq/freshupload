from flask import Flask, request, url_for, render_template, flash, redirect, jsonify
from flaskext.uploads import (UploadSet, configure_uploads, IMAGES, UploadNotAllowed)
from werkzeug import secure_filename
import platform, hashlib, datetime

app = Flask(__name__)

photos = UploadSet('photos', IMAGES, default_dest=lambda app: app.instance_root)

@app.route("/upload")
def hello():
	return render_template('upload.html')

@app.route("/view/<filename>")
def view(filename):
	return render_template('view.html', filename=filename, url=app.url)

@app.route('/v1/api/upload', methods=['POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		rand = hashlib.sha224(request.files['photo'].filename + str(datetime.datetime.now())).hexdigest()[:15]+"."
		filename = photos.save(request.files['photo'], name=rand)
		flash("Photo saved.")
		result = {
			"filename": filename,
			"directurl": app.url + url_for('static', filename=filename),
			"viewurl": app.url + url_for('view', filename=filename),
		}
		return jsonify(result)


if __name__ == "__main__":
	app.debug = True
	app.host = '0.0.0.0'
	app.port = '5000'
	app.url = 'https://%s' % platform.uname()[1]
	app.instance_root = './static/'
	app.secret_key = "7bH6^ugydHVVocwDjCb8y6n.L"
	configure_uploads(app, photos)
	app.run()
