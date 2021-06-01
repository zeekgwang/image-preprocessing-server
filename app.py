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
    df_image = pd.DataFrame({'f_name': os.listdir(f'static/img/freedraw/cropped/{epi}')})

    if not os.path.isdir(f'csv/freedraw/cropped/{epi}'):
        os.mkdir(f'csv/freedraw/cropped/{epi}')

    if not os.path.isfile(f'csv/freedraw/cropped/{epi}/{epi}.csv'):
        pd.DataFrame({'f_name': [],
                      'use_yn': []}).to_csv(f'csv/freedraw/cropped/{epi}/{epi}.csv')

    df = pd.read_csv(f'csv/freedraw/cropped/{epi}/{epi}.csv')

    df = pd.merge(df_image, df, how='left')
    df['use_yn'] = df['use_yn'].fillna('Y')

    return render_template('frame.html',
                           epi=epi,
                           file_name=df['f_name'],
                           use_yn=df['use_yn'],
                           enumerate=enumerate,
                           zip=zip,
                           next=next,
                           prev=prev)


@app.route("/save", methods=["POST"])
def save():
    params = request.get_json()
    # print(params['epi'])
    # print(params['file_name_list'])
    # print(params['use_yn_list'])

    df = pd.DataFrame({'f_name': params['file_name_list'],
                       'use_yn': params['use_yn_list']})

    df.to_csv(f'csv/freedraw/cropped/{params["epi"]}/{params["epi"]}.csv')

    return jsonify()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
