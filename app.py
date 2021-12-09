from flask import Flask
from flask import render_template,request,redirect,url_for
import tensorflow as tf
import pickle


app = Flask(__name__)


tokenizer_org = tf.keras.preprocessing.text.Tokenizer()
value_list = []


@app.route("/",methods =['GET','POST'])
def index():
    global value_list
    if request.method == 'POST':
        type_dict = {'cash_in':6,'cash_out':7,'debit':8,'payment':9,'transfer':10}
        print(request.form)
        amount = float(request.form['amount'])
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])
        oldbalanceDest = float(request.form['oldbalanceDest'])
        newbalanceDest = float(request.form['newbalanceDest'])
        try:
            if request.form['merchant'] == 'on':
                value =1
        except:
            value = 0
        value_list = [
        int(request.form['step']),
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        0,      0,        0,        0,        0,
        value,
        1 if round(abs(amount - abs(newbalanceOrig - oldbalanceOrg)),2) != 0 else 0,
        1 if round(abs(amount - abs( newbalanceDest - oldbalanceDest)),2) != 0 else 0,
        ]
        value_list[type_dict[request.form['type']]] = 1
        return redirect(url_for('result'))
        
    return render_template('index.html')

@app.route('/result')
def result():
    with open('MyFinalTransaction','rb') as file:
        model = pickle.load(file)
    pred = model.predict([value_list])
    return render_template('result.html',pred = pred,val = value_list)

#surge > amount
#freq_dest = 1 if multiple receivers
#merchant = 1 if merchant
# #orig_diff = 1 if  

# #step	amount	oldbalanceOrg	newbalanceOrig	oldbalanceDest	newbalanceDest	CASH_IN	CASH_OUT	DEBIT	PAYMENT	TRANSFER	Merchant	diff_Org	diff_Dest
# diff_Orig = 1 if round(abs(amount - abs(newbalanceOrig-oldbalanceOrig)),2) != 0  else 0
# diff_Dest = 0 if round(abs(amount - abs(newbalanceDest-oldbalanceDest)),2) != 1 else 1
# surge = 1 if amount > 450000 else 0
