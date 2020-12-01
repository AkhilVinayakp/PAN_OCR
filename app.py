import os
import requests
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import re, datetime
# the following program is the backend of pan card ocr program. API used is 'https://api.ocr.space/parse/image'
# static folder in the project directory is used for storing the uploaded images
Up_folder = os.path.join(os.getcwd(), 'static')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(Up_folder)
extensions = ('png', 'jpeg', 'jpg')  # supported image extension tuple


# checking whether the extension of uploaded image is one of the extensions declared above
def in_extension(file):
    return True if '.' in file and file.rsplit('.')[1] in extensions else False


#  http://127.0.0.1:5000 will be the url path for the website
@app.route('/', methods=['GET', 'POST'])
def run_ocr():
    if request.method == 'POST':
        if request.files:
            image = request.files['file']
            if image.filename == "":
                print('does not have a file name')
                return redirect(request.url)
            if not in_extension(image.filename):
                print('extension not supported')
                return redirect(request.url)
            file_name = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            print('ok')
            err_code, err_text, par_text = ocr_space_file(file_name, overlay=False, api_key='1460742ff688957',
                                                          language='eng')
            if err_code is True:
                return render_template('error.html', error=err_text)
            par_text = par_text.split('\r\n')
            name = 'can not extract'
            dob = 'can not extract'
            pan = 'can not extract'
            # trying to extract the data using regular expression
            try:
                s = " ".join(par_text)
                match = re.search('\d{2}/\d{2}/\d{4}', s)
                date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
                print(s, date)
                dob = date
                name = par_text[1]
                for i, text in enumerate(par_text):
                    if bool(re.match('(?=.*[0-9])(?=.*[a-zA-Z])', text)):
                        print(par_text[i])
                        pan = par_text[i]
            except Exception as e:
                print('error in exception')
            return render_template("result.html", img=file_name, name=name, dob=dob, pan=pan)
    return render_template("upload.html")


#  function for using api the parsed result will send back
def ocr_space_file(filename, overlay=False, api_key='test', language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language
    }
    print(os.getcwd())
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload)
        t = r.json()
        print(r.status_code)
        print(r.json())
        print(t['IsErroredOnProcessing'])
        print(t['ParsedResults'][0]['ParsedText'])
        return t['IsErroredOnProcessing'], t['ParsedResults'][0]['ErrorMessage'], t['ParsedResults'][0]['ParsedText']


if __name__ == '__main__':
    app.run(debug=True)
