
from flask import Flask, render_template, request
from trial import unfound
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        phrase=request.form.getlist('name')
        sentences=request.form.getlist('sentences')
        print(phrase)
        result=unfound(phrase[0],sentences[0])
        print(result)
        return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)
