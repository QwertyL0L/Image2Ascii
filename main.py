from flask import Flask, render_template, request, redirect, make_response
from werkzeug.utils import secure_filename
from ascii_magic import AsciiArt

UPLOAD_FOLDER = '/home/runner/image2ascii/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        my_art = AsciiArt.from_image(path=f"{app.config['UPLOAD_FOLDER']}/{filename}")
        my_html_markup = my_art.to_html(full_color=True, columns=200)
        return render_template('result.html', ascii_art=my_html_markup, filename=filename)
    else:
        return redirect(request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
