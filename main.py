# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import Required
from flask_wtf.csrf import CsrfProtect
from flask_bootstrap import Bootstrap
import uuid


UPLOAD_FOLDER = "./upload"
access_key = "HoId5fqVevUfPOgZtxgoHmD2l72dPGWcMOB60rMY"
secret_key = "srcLOV3vFMVzeFXpGj5755CBPUHyDzLPfgGLmajs"
PATH = "http://oisjm47jk.bkt.clouddn.com/"
i = 1

app = Flask(__name__)
app.config['SECRET_KEY']="a random string"
CsrfProtect(app)
Bootstrap(app)

class inputForm(Form):
    file_name_1 = StringField(u'请填写第一张照片的路径:', validators=[Required()])
    file_name_2 = StringField(u'请填写第二张照片的路径:', validators=[Required()])
    submit = SubmitField(u'提交')


class imageForm(Form):
    image1 = StringField(validators=[Required()])
    image2 = StringField(validators=[Required()])


@app.route('/', methods=['GET', 'POST'])
def index():
    inputform = inputForm()
    if inputform.is_submitted():
        url1 = upload(inputform.file_name_1.data)
        url2 = upload(inputform.file_name_2.data)
        return redirect(url_for('check', pic1=url1, pic2=url2))

    return render_template('main.html', form=inputform)


@app.route('/result/<string:pic1>/<string:pic2>', methods=['GET', 'POST'])
def check(pic1, pic2):
    pic1 = PATH+pic1
    pic2 = PATH+pic2
    import requests
    data = {
        "api_key": "dmmlji2YGL9ljSKJ9QXEK32uvlCtQTGm",
        "api_secret": "Q-OxI9LAvztoGPpZUp2haH11M2-5CWHY",
        "image_url1": pic1,
        "image_url2": pic2
    }
    url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'

    r = requests.post(url=url, data=data)

    result = r.json()

    threshold = result["confidence"]
    print threshold

    if threshold > 50.0:
        flash("Seems like these two poor guys are the one")
    else:
        flash("A~O! Not the same persion.")
    return render_template('result.html', pic1=pic1, pic2=pic2)


def upload(url):
    from qiniu import Auth, put_file

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'jiangfeng'

    # 上传到七牛后保存的文件名
    key = str(uuid.uuid1()) + '.jpg';

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key)

    # 要上传文件的本地路径
    localfile = url

    ret, info = put_file(token, key, localfile)

    print key

    return key


if __name__ == '__main__':
    app.run(debug=True)

