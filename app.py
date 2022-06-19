import pandas as pd
from flask import Flask, request, render_template

import model as model

app = Flask(__name__, template_folder='template')
app.static_folder = 'static'


# Render to Homepage
@app.route('/')
def homepage():
    return render_template('home.html', name='home')


# Render to Upload Page
@app.route('/result/', methods=['GET', 'POST'])
def process_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        if file:
            # Read File
            df = pd.read_excel(file)
            # check radio button value
            if request.form['checkbox'] == 'Continuous Gas Flow':
                model.continuous_data(df)
            else:
                model.store_series_data(df)
        return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    app.env = 'development'

