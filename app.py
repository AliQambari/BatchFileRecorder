from flask import Flask
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from werkzeug.utils import secure_filename
import dropbox
import shutil
import pathlib


import os
import uuid

app = Flask(__name__)
app.secret_key = "@aqa96df#AQAQ"
dbx = dropbox.Dropbox("sl.BRtHpEqGzZZ7PMJ-78eiTgm0GNBvA4Lwr85KeQMJR3FC88A3khdi9M406VFZARJnmesR7RPzXhJ33dFdpCFQ4SCsUnv-NtgbxGRSQQQ9-YCU0BEE8KEg4G0Ph2eEvfAnLLZT8eFKa7g")


@app.route("/")
def welcome():
    session_id = request.cookies.get('session_id')
    if session_id:
        all_done = request.cookies.get('all_done')
        if all_done:
            return render_template("thanks.html")
        else:
            return render_template("record.html")
    else:
        return render_template("welcome.html")

@app.route("/legal")
def legal():
    return render_template("legal.html")

@app.route("/start")
def start():
    response = make_response(redirect('/'))
    session_id = uuid.uuid4().hex
    response.set_cookie('session_id', session_id)
    return response

@app.route('/upload', methods=['POST'])
def upload():
    session_id = request.cookies.get('session_id')
    if not session_id:
        make_response('No session', 400)
    word = request.args.get('word')
    audio_data = request.data
    filename = word + '_' + session_id + '_' + uuid.uuid4().hex + '.wav'
    secure_name = secure_filename(filename)
    # Left in for debugging purposes. If you comment this back in, the data
    # will be saved to the local file system.
    from pathlib import Path
    p = Path('./output/')
    p.mkdir(exist_ok=True)
    """
    with open(secure_name, 'wb') as f:
            f.write(audio_data) 
            """
    with (p / secure_name).open('wb') as fp2:
            fp2.write(audio_data)   
                 
    shutil.make_archive('zipped', 'zip','./output')
    
      
    local_file = zipped.zip
    with open(local_file, 'rb') as f:
            dbx.files_upload(f.read(), path=f"/aq/zipped.zip", mode=dropbox.files.WriteMode.add)
     

        
   # upload gives you metadata about the file
   # we want to overwite any previous version of the file
  # Create a Cloud Storage client
    """.
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(secure_name)
    blob.upload_from_string(audio_data, content_type='audio/ogg')
    """
    return make_response('All good')

# CSRF protection, see http://flask.pocoo.org/snippets/3/.
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session['_csrf_token']
        if not token or token != request.args.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == "__main__":
     app.run(debug=True)
     app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
