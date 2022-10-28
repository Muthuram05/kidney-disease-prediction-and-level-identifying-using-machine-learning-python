from flask import Flask, render_template, request
import numpy as np
import pickle


app = Flask(__name__)
model = pickle.load(open('Kidney.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])
        values = np.array([[sg, htn, hemo, dm, al, appet, rc, pc]])
        prediction = model.predict(values)
        return render_template('result.html', prediction=prediction)


@app.route("/stage", methods=['GET'])
def stage():
    return render_template('stage.html')

@app.route("/kidneyDisease",methods=['GET'])
def kidneyDisease():
    return render_template('kidneyDisease.html')

@app.route("/stageIdenty",methods=['POST'])
def stageIdenty():
    gender=request.form['gender']
    age=int(request.form['age'])
    wt=int(request.form['wt'])
    cretinine=float(request.form['cretinine'])
    up = (140 - age) * wt
    down = 72*cretinine
    res = up // down 
    if gender == 'Female':
        feres=res * 0.85
        gen=feres
    else:
        gen=res

    if gen>90:
        val="Stage 1:"
        #89 to 60
    elif(60<=gen<=89):
        val="stage 2:"
        #59 to 45
    elif(45<=gen<=59):
        val="stage 3A:"
        #44 to 30
    elif(30<=gen<=44 ):
        val ="stage 3B"
        #29 to 15
    elif(15<=gen<=29):
        val="stage 4:"
    else:
        val="stage 5:"
    return render_template('stageResult.html',val=val)

if __name__ == "__main__":
    app.run(debug=True)

