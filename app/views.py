from flask import render_template, flash, request, abort, send_from_directory
import matplotlib.pyplot as plt
import numpy as np
import os
import io
import cv2
from skimage.color import rgb2gray
from scipy import ndimage
from app import app



#prevent XSS attack - user is not allowed to upload html
ALLOWED_EXTENSIONS = ['pdf', 'tiff', 'jpg', 'jpeg', 'gif','png']



def delete_image_from_directory():
    '''
    deleting old image every time after ruturning to home page
    '''
    filename = "image.jpg"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if os.path.isfile(image_path):
        os.remove(image_path)
    

def allowed_file(filename):
    '''
    check whether our filename meet allowed file extensions
    '''
    if filename[-3:].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def load_picture():
    '''
    loading data from the img folder at the disposal of image processing function
    '''
    try:
        filename = "image.jpg"
        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename),-1)
        # imread returns image in BRG format by default, convert it to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except FileNotFoundError:
        abort(404)


def kernels(option):    
    '''
    all possible kernels in our application
    '''
    kernels = {
        'sharpen': np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        'blur': np.full((3, 3), 1/9),
        'sobel-vertical': np.array([[-1, 0, -1], [-2, 0, 2], [-1, 0, 1]]),
        'sobel-horizontal': np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),
        'laplace': np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    }
    if option in kernels:
        return kernels[option]
    else:
        return None


@app.route('/')
def home():
    '''
    rendering home page
    '''
    
    return render_template('index.html'), delete_image_from_directory()

@app.route('/upload-image' , methods=['GET', 'POST'])
def upload_image():
    '''
    uploading an image and saving it to img folder in static directory
    checking if an user picked an image and pressed the upload button
    '''
    #first check whether is there any old image, if yes delete it
    
    
    upload = False
    if request.method == 'POST':
        try:
            if request.files and request.form:
                image = request.files['image']
                upload = request.form['upload']
                if allowed_file(str(image.filename)) and upload:
                    in_memory_file = io.BytesIO()
                    image.save(in_memory_file)
                    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
                    color_image_flag = -1
                    img = cv2.imdecode(data, color_image_flag)
                    filename = "image.jpg"
                    cv2.imwrite((os.path.join(app.config['UPLOAD_FOLDER'], filename)),img)
                    return ('', 204)
                else:
                    flash("unauthorized file extension or you did not choose a file")
                    return render_template('index.html')
        except:
            return render_template('index.html')
    else:
        abort(404)
 
@app.route('/image-processing', methods=['GET','POST'])
def image_processing():
    '''
    loading an image using load_picture() function
    applying a selected kernel to the picture saving and displaying using display_image() funtion
    '''       
    try:
        if request.method == 'POST':
            img = load_picture()
            #option = request.form['sharpen']
            option = request.form['kernel']
            cmap = request.form['colormap']
            # picking our kernel, using helper function 
            kernel = kernels(option)
            # asking ndarray if the matrix is not empty 
            if kernel.size:    
                # turning image into grayscale (from rgb to grayscale)
                gray = rgb2gray(img)
                # applying 2d kernel on 2d (grayscale) images
                img = ndimage.convolve(gray, kernel, mode='reflect') 
                filename = "image.jpg"
                plt.imsave((os.path.join(app.config['UPLOAD_FOLDER'], filename)),img, cmap=cmap)
                return render_template('processed_image.html',filename=filename, kernel=option)
        else:
            abort(404)
                    
    except:
        flash("you did not choose a kernel/colormap or you did not press the upload button, please try it again")
        return render_template('index.html')
             
        
            
@app.route('/display-image/<filename>')
def display_image(filename):
    '''
    displaying an image to a page after applying a given kernel
    '''
    try:
        return send_from_directory(
            # as attachment True allows download the image
            app.config['PROCESSED_IMAGE'],filename= filename,  as_attachment=False
            )
            
    except FileNotFoundError:
        abort(404)
        
