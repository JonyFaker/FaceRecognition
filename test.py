# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag

#需要填写你的 Access Key 和 Secret Key
access_key = "HoId5fqVevUfPOgZtxgoHmD2l72dPGWcMOB60rMY"
secrect_key = "srcLOV3vFMVzeFXpGj5755CBPUHyDzLPfgGLmajs"

#构建鉴权对象
q = Auth(access_key, secrect_key)

#要上传的空间
bucket_name = 'jiangfeng'

#上传到七牛后保存的文件名
key = 'my-python-logo.png';

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key)

#要上传文件的本地路径
localfile = '/Users/jiangfeng/Downloads/ours/0身份证/常满禹.jpg'

ret, info = put_file(token, key, localfile)
print info
assert ret['key'] == key
assert ret['hash'] == etag(localfile)

