
from flask import Flask, render_template, request,send_file,redirect
from werkzeug.utils import secure_filename
import json
import requests
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
import bcrypt
import pymongo
# import python_jwt as jwt, jwcrypto.jwk as jwk, datetime


app = Flask(__name__)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(app)
cluster = pymongo.MongoClient('mongodb+srv://phattaraphon:0989153312@cluster0.trckf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# cluster = pymongo.MongoClient('mongodb+srv://phattaraphon:0989153312@cluster0.trckf.mongodb.net/flutter?retryWrites=true&w=majority')
db = cluster.flutter
collection = db.test
dbUser = db.User
print(cluster.list_database_names())
@app.route('/')
def hello_world():
    tt = str(cluster.list_database_names())
    return tt
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      # filename = secure_filename(f.filename)
      # f.save(os.path.join("files/",filename))
      headers = {"Authorization": "Bearer ya29.a0AfH6SMDT7CvvI-GDh-2yOZn3jGGpfEHPPZKCQl1zCrfWMPe7xm0R5vOUzWjv61tGP4ZqJCHFBwRYKPF7gc-iXkh0j63pJifm9WSRvgKb3zpnQP-1hJdjDcpxiddE_L0fbvzZioMD4L8JhnRjleuQgsHI8N7O8pBfbeOiPV6Y3Ck"}
      para = {"name": f.filename,
              "parents": ["1lMBii79CfFiG7t9KcUS0cB-4EvmpV8Pf"]
            }
      files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
               'file': f
            }
      r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",headers=headers,files=files)
      print(r.json()['id'])
    #   f.save(secure_filename("files/"+f.filename))
      return 'file uploaded successfully'
@app.route('/download/<string:name>')
def downloadFile(name):
    return redirect("https://drive.google.com/uc?id=1kuvr_4TftRo9uI8oIhojdWRKr5Hjt3_d&export=download",code=302)


@app.route('/signup', methods = ['GET', 'POST'])
def singup():
  if request.method =='POST':
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password'].encode('utf-8')
    checkemail = dbUser.find({'email': email})
    print(name,email,password)
    try:
      yy = checkemail[0]
      print("มี")
      return "this email has already been used"
    except:
      print("ไม่มี")
      salt = bcrypt.gensalt()
      hashed = bcrypt.hashpw(password,salt)
      p = hashed.decode()
      dbUser.insert_one({'name':name,'email':email,'password':p})
      return "success"
@app.route('/signin', methods = ['GET', 'POST'])
def singin():
  if request.method =='POST':
    data = request.get_json()
    email = data['email']
    password = data['password'].encode('utf-8')
    user = dbUser.find({'email':email})
    try :
      yy = user[0]['email']
      try:
        passdb = user[0]['password'].encode('utf-8')
        if bcrypt.checkpw(password,passdb):
          print("match")
          ids = str(user[0]['_id'])
          name = str(user[0]['name'])
          email = str(user[0]['email'])
          # key = jwk.JWK.generate(kty='RSA', size=2048)
          # key = ''
          # payload = { 'id': ids, 'name': name,"email":email }
          # token = jwt.generate_jwt(payload, key, 'HS256')
          # token = jwt.encode({'id': ids, 'name': name,'email': email},key="",algorithm="HS256")
          # return "Match"
          # return {'status':'singin success',"id":ids,"name":name,"email":email}
          token = create_access_token({ 'id': ids, 'name': name,"email":email })
          return {'status':'singin success','token':token}
        else:
          print("does not match")
          return {'status':'password is incorrectsssss'}
      except:
        return {'status':'password is incorrect'}
            
    except:
      return {'status':'invalid email'}
if __name__ == '__main__':
   app.run(debug = True)
