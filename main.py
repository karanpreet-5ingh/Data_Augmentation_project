from flask import Flask, render_template, request,send_file
import cv2
import os
import zipfile
import numpy as np
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("login.html")
database={'karan':'123','james':'aac','karthik':'asdsf'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
            return render_template('upload.html')





@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Save the file to a temporary location
        file.save('./temp/temp.jpg')

        # Open the image using OpenCV
        img = cv2.imread('./temp/temp.jpg')

        # Apply data augmentation techniques here...
        # For example, you can rotate the image by 45 degrees using the following code:
        rows, cols = img.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 45, 1)
        rotated_img = cv2.warpAffine(img, M, (cols, rows))

        # Flip the image horizontally
        flipped_image = cv2.flip(img, 1)

        # Rotate the image by 90 degrees clockwise
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        ninty_deg_rotated_image = cv2.warpAffine(img, M, (w, h))

        # Scale the image by a factor of 2
        scaled_image = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Crop the image
        cropped_image = img[100:200, 100:200]


        # Convert the image to grayscale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Equalize the histogram of the image
        equalized_image = cv2.equalizeHist(gray_image)


        # Adjust the gamma of the image
        gamma = 2.0
        lookup_table = np.empty((1,256), np.uint8)
        for i in range(256):
            lookup_table[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
        gamma_adjusted_image = cv2.LUT(img, lookup_table)

        # Add Gaussian noise to the image
        noisy_image = img + np.random.normal(0, 25, img.shape)        

        # Blur the image using a 3x3 kernel
        blurred_image = cv2.GaussianBlur(img, (3, 3), 0)

        

        # Save the augmented image to a new file
        cv2.imwrite('./temp/rotated.jpg', rotated_img)
        cv2.imwrite('./temp/flipped_image.jpg', flipped_image)
        cv2.imwrite('./temp/ninty_deg_rotated_image.jpg', ninty_deg_rotated_image)
        cv2.imwrite('./temp/scaled_image.jpg', scaled_image)
        cv2.imwrite('./temp/cropped_image.jpg', cropped_image)
        cv2.imwrite('./temp/gray_image.jpg', gray_image)
        cv2.imwrite('./temp/equalized_image.jpg', equalized_image)
        cv2.imwrite('./temp/gamma_adjusted_image.jpg', gamma_adjusted_image)
        cv2.imwrite('./temp/noisy_image.jpg', noisy_image)
        cv2.imwrite('./temp/blurred_image.jpg', blurred_image)

        # Create a zip file
        zip_file = zipfile.ZipFile('./temp/augmented_images.zip', 'w')

        # Add the augmented images to the zip file
        zip_file.write('./temp/temp.jpg', 'original.jpg', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/rotated.jpg', 'rotated.jpg', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/flipped_image.jpg' , 'flipped_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/ninty_deg_rotated_image.jpg', 'ninty_deg_rotated_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/scaled_image.jpg', 'scaled_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/cropped_image.jpg', 'cropped_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/gray_image.jpg', 'gray_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/equalized_image.jpg', 'equalized_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/gamma_adjusted_image.jpg', 'gamma_adjusted_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/noisy_image.jpg', 'noisy_image', compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('./temp/blurred_image.jpg', 'blurred_image', compress_type=zipfile.ZIP_DEFLATED)
        

        # Close the zip file
        zip_file.close()

        # Render the download page with the download button
        return render_template('download.html')
    else:
        # Render the upload page
        return render_template('upload.html')

@app.route('/download')
def download_file():
    # Send the zip file as a response
    return send_file('./temp/augmented_images.zip', as_attachment=True)

@app.route("/redirect", methods=["POST"])
def redirect_page():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=1)
