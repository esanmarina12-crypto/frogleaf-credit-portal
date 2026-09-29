import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

credit_records = []

@app.route('/')
def index():
    return render_template('index.html', records=credit_records)

@app.route('/upload', methods=['POST'])
def upload_bill():
    card_id = request.form.get('cardId')
    customer_name = request.form.get('customerName')
    amount = request.form.get('amount')
    file = request.files.get('billImage')

    filename = ""
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    record = {
        'card_id': card_id,
        'customer_name': customer_name,
        'amount': amount,
        'image': filename
    }
    credit_records.insert(0, record)

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
