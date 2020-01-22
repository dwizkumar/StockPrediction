from flask import Flask, render_template, request, redirect, flash
from testPrediction import PredictData

app = Flask(__name__)

@app.route('/')
def index():
    """
     Loads the homepage
    """
    return render_template("/html/home.html")

@app.route('/Check_result', methods = ['GET','POST'])
def check():
    """
      Returns table data
    """
    comp_name = request.form['comp_name']
    predictData = PredictData()
    pred_Lists, feature_Lists, pos_score, neg_score, neut_score = predictData.test_predict(comp_name)
    neut_score = int(neut_score)
    neg_score = int(neg_score)
    pos_score = 100 - (neut_score + neg_score)
    # print(pred_Lists)
    # print(feature_Lists)
    # print(pos_score)
    # print(neg_score)
    # print(neut_score)
    pred_Lists.sort(key=lambda x: x[1], reverse = True)
    #return redirect("http://localhost:5000", data = pred_Lists ,code=302)
    return render_template("/html/home.html", pred_Lists = pred_Lists, feature_Lists = feature_Lists, pos_score = pos_score,
                           neg_score = neg_score, neut_score = neut_score)

if __name__ =='__main__':
    app.run(debug=True)
