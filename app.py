import os
import PyPDF2
import re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set([ 'pdf'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

def data(ab): 
  dataa = ''
  for i in ab:
    if i == '.':
      x = ab.index(i)
      #print(x)
  dataa = ab[:x]+ab[x:x+4]
  return float(dataa)
  

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file")
    total_no_of_pages = 0 
    dict = {}
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            contents = file.read()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Pdf = PyPDF2.PdfFileReader(file)
            NumPages = Pdf.getNumPages()
            total_no_of_pages += NumPages


            for i in range(0, NumPages):

              PageObj = Pdf.getPage(i)
              total = PageObj.extractText()
              
              string = total
              pattern = 'JIO'
              finall = [match.start() for match in re.finditer(pattern, string)] 

    #find the date 
              for j in finall:
                abc = ''
                for i in range(j-36, j):
                  abc +=total[i]
                  dates = abc[:9]
    #find the data used

                abcd = ''
                for k in range(j+6 , j+15):
                  abcd += total[k]
                datas = data(abcd)

    #push it into dictionary and calculates the data 
                if dates in dict:
                  dict[dates] = dict.get(dates) + datas
     
                else:
                  dict[dates] = datas
                    
        
                
            
            
    total = 'total no fo pages = ' + str(total_no_of_pages )
    average = str('average data used = ')+str(sum(dict.values())/len(dict))

    return render_template('index.html' , result1= total , result2 = average ) 


