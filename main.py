from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import requests
from werkzeug.utils import secure_filename
import os
import PyPDF2

app = Flask(__name__)

### esto es para el Flask, sin esto genera error
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


API_KEY = "YOUR API KEY"
END_POINT = "http://api.voicerss.org/?"




UPLOAD_FOLDER = '//uploads'
ALLOWED_EXT = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# @app.route("/hear", methods=['GET'])
# def hear():

#     return render_template('hear.html')



# def get_wav():

#     response = requests.get(
#         url=END_POINT,
#         # headers=headers,
#         params=headers
#     )

#     print(response)
#     print(response.encoding)
#     print(response.content)
#     # print(response.json())

#     with open("my_file.wav", 'wb' ) as file:
#         file.write(response.content)



@app.route("/", methods=['GET', 'POST'])
def home():


    
    # print(response)
    # print(response.encoding)
    # print(response.content)
    # print(response.json())

    # with open("my_file.wav", 'wb' ) as file:
    #     file.write(response.content)



    if request.method == 'POST':
        ### check if the post request has the file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        ### if the user does not select a file, the browser submits
        ### and empty file without name
        # print(file)

        if file.filename == '':
            flash('No selected file')
            return redirect (request.url)

        #print("Allowed file", allowed_file(file.filename))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print("OS PATH", os.path.join(app.config['UPLOAD_FOLDER']))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER']), filename)
            #print("CONTENT TYPE",file.content_type)
            
            pdf_read = PyPDF2.PdfReader(file)
            
            print()  #### aquí ya está el texto a reproducir


            ##### ahora meter el texto y traer el wav de la API

            headers={
                "key" : API_KEY,
                "src" : pdf_read.pages[0].extract_text(),
                "hl" : "en-us"
            }

            response = requests.get(
                url=END_POINT,
                # headers=headers,
                params=headers
            )

            #### borrar antes de crear el nuevo
            try:
                os.remove("./static/my_file.wav")
            except:
                pass


            with open("./static/my_file.wav", 'wb+' ) as file:
                file.write(response.content)


            return render_template('hear.html')
        
            return redirect(url_for('download_file'), name=filename)

        

    return render_template('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
