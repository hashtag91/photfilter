from flask import Flask, render_template, request, url_for, Response, send_file, json, redirect
import os, io, cv2

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['TEMP_FOLDER'] = 'static/temp/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

img_array = None
filename = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    global filename
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(file_path)
    global img_array
    img_array = cv2.imread(file_path)
    filters = ['blur','canny','gray','original','threshold']
    for f in filters:
        img = image_filter(f)
        path = os.path.join(app.config['TEMP_FOLDER'],f'{f}.jpg')
        cv2.imwrite(path, img)
    return render_template('index.html',img_path = file_path)

def image_filter(img_filter):
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img_array, (15,15),0)
    _,thres = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if img_filter == 'gray':
        image_proceed = gray
    elif img_filter == 'blur':
        image_proceed = blurred
    elif img_filter == 'threshold':
        image_proceed = thres
    elif img_filter == 'canny':
        image_proceed = cv2.Canny(thres,160.0, 255.0)
    else:
        image_proceed = img_array
    return image_proceed

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    img_filter = request.form.get('filter')
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],filename)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return Response(json.dumps({'path':f'static/temp/{img_filter}.jpg'}), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)