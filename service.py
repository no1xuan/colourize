import time
import os
import base64
from flask import Flask, jsonify
from utils.form_models import ImageForm
from datetime import timedelta
from color_transformer import img_transformer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PAPERCLUBASDFASDF'
app.config['WTF_CSRF_ENABLED'] = False  # 关闭CSRF保护
app.send_file_max_age_default = timedelta(seconds=1)
app.config['UPLOAD_FOLDER'] = './tempImgs/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def img2byte(img_path):
    # 读取文件并返回字节流，文件过大时使用生成器逐块读取
    with open(img_path, 'rb') as f:
        return f.read()

def process_and_cleanup(img_filepath):
    try:
        # 图像处理
        ori_bytes = img2byte(img_filepath)
        img_bytes = img_transformer(ori_bytes, method=1)

        return img_bytes
    finally:
        # 删除临时图像文件
        if os.path.exists(img_filepath):
            os.remove(img_filepath)

@app.route('/colourizeImg', methods=['POST'])
def main():
    form = ImageForm()

    if form.validate_on_submit():
        base64_data = form.base64_image.data
        img_data = base64.b64decode(base64_data.split(',')[1])
        filename = f"uploaded_{time.time()}.png"
        img_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 将图像保存为临时文件
        with open(img_filepath, 'wb') as f:
            f.write(img_data)

        # 处理图像并清理临时文件
        img_bytes = process_and_cleanup(img_filepath)

        response_data = {
            "status": 2,  # 2成功，1失败
            "processed_image": img_bytes
        }

        return jsonify(response_data)
    else:
        errors = [error for error in form.errors.values()]
        response_data = {
            "status": 1,
            "message": errors
        }

        return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3007, debug=True)
