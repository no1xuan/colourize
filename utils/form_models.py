#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ Date    : 2022/7/7 20:55
# @ Author  : DELL
# @ Site    : 
# @ Software: PyCharm
import base64
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators, ValidationError

class ImageForm(FlaskForm):
    """ 只接收Base64编码图片 """
    base64_image = TextAreaField(label='Base64 Encoded Picture', validators=[validators.DataRequired()])
    submit = SubmitField('点击上传图片')

    def validate_base64_image(self, field):
        base64_data = field.data
        try:
            img_data = base64.b64decode(base64_data.split(',')[1])
            file_extension = self.get_image_extension(img_data)
            if file_extension not in ['.png', '.jpg', '.jpeg', '.bmp']:
                return ValidationError('请上传有效的图片文件（支持png、jpg、jpeg、bmp格式）')
        except Exception as e:
            return ValidationError(f'图片数据无效: {str(e)}')

    def get_image_extension(self, img_data):
        """
        根据图片数据的前几个字节判断图片格式，返回对应的后缀名
        """
        if img_data.startswith(b'\x89PNG\r\n\x1a\n'):
            return '.png'
        elif img_data.startswith(b'\xff\xd8') and img_data.endswith(b'\xff\xd9'):
            return '.jpg'
        elif img_data.startswith(b'\xff\xd8') and img_data.endswith(b'\xff\xd9'):
            return '.jpeg'
        elif img_data.startswith(b'BM'):
            return '.bmp'
        return None



