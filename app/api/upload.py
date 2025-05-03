from flask import request, jsonify
from app.api import api_bp
import os

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    上传文件接口
    """
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '没有文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': '未选择文件'}), 400
    filename = file.filename
    save_path = os.path.join('/tmp', filename)
    file.save(save_path)
    return jsonify({'code': 200, 'message': '上传成功', 'filename': filename})
  