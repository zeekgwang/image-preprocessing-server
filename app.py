from flask import Flask, render_template, request, jsonify

import os
import pandas as pd

app = Flask(__name__)


def next(x):
    return int(x) + 1


def prev(x):
    return int(x) - 1


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/freedraw/<epi>', methods=['GET'])
def freedraw(epi):
    print(epi)

    return render_template('frame.html',
                           epi=epi,
                           file_name=os.listdir(f'static/img/freedraw/cropped/{epi}'),
                           use_yn=['N', 'N', 'Y', 'N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'],
                           enumerate=enumerate,
                           zip=zip,
                           next=next,
                           prev=prev)


@app.route("/save", methods=["POST"])
def save():
    params = request.get_json()
    print(params['epi'])
    print(params['file_name_list'])
    print(params['use_yn_list'])

    df = pd.DataFrame({'file_name_list': params['file_name_list'],
                       'use_yn_list': params['use_yn_list']})

    save_csv(df)

    return jsonify({'name': 'Alice', 'birth-year': 1986})


def save_csv(df):
    print(os.getcwd())
    df.to_csv(f'/csv/use.csv')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
