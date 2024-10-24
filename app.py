import os
import numpy as np
from PIL import Image
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.applications.vgg16 import preprocess_input # type: ignore

app = Flask(__name__)

# Tải mô hình đã được huấn luyện
model_path = 'weights/vgg16_model.h5'  # Đảm bảo mô hình đã tồn tại
model = load_model(model_path)

def get_className(classNo):
    if classNo == 0:
        return "Có u não"
    elif classNo == 1:
        return "Không có u não"

def getResult(img_path):
    try:
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError("Không thể đọc hình ảnh, vui lòng kiểm tra định dạng tệp.")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Chuyển đổi màu sắc
        image = Image.fromarray(image)
        image = image.resize((128, 128))
        image = np.array(image)
        image = preprocess_input(image)  # Chuẩn hóa hình ảnh
        input_img = np.expand_dims(image, axis=0)
        result = model.predict(input_img)
        result01 = np.argmax(result, axis=1)
        return result01[0]  # Trả về giá trị đầu tiên của mảng
    except Exception as e:
        print(f"Lỗi trong quá trình xử lý hình ảnh: {str(e)}")
        raise e

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return "Không có tệp nào được tải lên", 400
        
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        
        try:
            f.save(file_path)
            # In ra thông tin với mã hóa UTF-8
            print(f"Tệp đã được lưu tại: {file_path}")  
            
            value = getResult(file_path)
            result = get_className(value) 
            return result
        except Exception as e:
            print(f"Đã xảy ra lỗi: {str(e)}")  # In ra lỗi
            return f"Đã xảy ra lỗi trong quá trình dự đoán: {str(e)}", 500
    return None

if __name__ == '__main__':
    app.run(debug=True)
