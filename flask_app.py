
from flask import Flask, render_template, request,send_file
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!888'


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join("files/",filename))
    #   f.save(secure_filename("files/"+f.filename))
      return 'file uploaded successfully'
@app.route('/download/<string:name>')
def downloadFile(name):
    return send_file("files/"+name, as_attachment=True)
if __name__ == '__main__':
   app.run(debug = True)
