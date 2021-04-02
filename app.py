import flask
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


#load models at top of app to load into memory only one time
with open('models/rf.pickle', 'rb') as f:
    clf_individual = pickle.load(f)

ss = StandardScaler()

df_macro_mean=pd.DataFrame(columns=['Age',  'Income', 'CreditScore',
       'HouseholdSize', 'State', 'MedianHomeValue',
       'MedianHouseholdIncome', 'Debt', 'LoanTerm', 'InterestRate',
       'CreditIncidents', 'HomeValue', 'LoanAmount', 'ProductType'])
df_macro_std =pd.DataFrame(columns=['Age',  'Income', 'CreditScore',
       'HouseholdSize', 'State', 'MedianHomeValue',
       'MedianHouseholdIncome', 'Debt', 'LoanTerm', 'InterestRate',
       'CreditIncidents', 'HomeValue', 'LoanAmount', 'ProductType'])


app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    return (flask.render_template('index.html'))

@app.route('/report')
def report():
    return (flask.render_template('report.html'))



@app.route("/Individual", methods=['GET', 'POST'])
def Individual():

    if flask.request.method == 'GET':
        return (flask.render_template('Individual.html'))

    if flask.request.method =='POST':


        Age = float(flask.request.form['code'])
        Income = float(flask.request.form['fico_avg_score'])
        CreditScore = float(flask.request.form['loan_amnt'])
        HouseholdSize = float(flask.request.form['term'])
        State = float(flask.request.form['dti'])
        MedianHomeValue = float(flask.request.form['home_ownership'])
        MedianHouseholdIncome = float(flask.request.form['mort_acc'])
        Debt = float(flask.request.form['annual_inc'])
        LoanTerm= float(flask.request.form['open_acc'])
        InterestRate = float(flask.request.form['verification_status'])
        CreditIncidents	 = float(flask.request.form['revol_util'])
        HomeValue = float(flask.request.form['total_acc'])
        LoanAmount = float(flask.request.form['er_credit_open_date'])
        ProductType = float(flask.request.form['er_credit_open_date'])


        temp = pd.DataFrame(index=[1])
        temp['term']=term
        temp['sub_grade']=sub_grade
        temp['home_ownership']=home_to_int[home_ownership.upper()]
        temp['annual_inc']=np.log(annual_inc)
        temp['verification_status']=verification_status
        temp['dti']=dti
        temp['revol_util']=revol_util
        temp['mort_acc'] = mort_acc
        temp['credit_hist']=credit_hist.days
        temp['credit_line_ratio']=credit_line_ratio
        temp['balance_annual_inc']=balance_annual_inc
        temp['fico_avg_score'] = fico_avg_score
        temp['inst_amnt_ratio']=inst_amnt_ratio

        #create original output dict
        output_dict= dict()
        output_dict['Provided Annual Income'] = annual_inc
        output_dict['Provided FICO Score'] = fico_avg_score
        output_dict['Predicted Interest Rate'] = int_rate * 100 #revert back to percentage
        output_dict['Estimated Installment Amount']=installment
        output_dict['Number of Payments'] = 36 if term==1 else 60
        output_dict['Sub Grade']= sub_grade_to_char[35-int(sub_grade)]
        output_dict['Loan Amount']=loan_amnt

        #create deep copy
        scale = temp.copy()
        for feat in df_macro_mean.columns:
            scale[feat] = (scale[feat] - df_macro_mean.loc[code,feat]) / df_macro_std.loc[code,feat]


        #make prediction
        pred = clf_individual.predict(scale)


        res = f'Congratulations! Approved! with probability {pred}'



        #render form again and add prediction
        return flask.render_template('Individual.html',
                                     original_input=output_dict,
                                     result=res,
                                     )



if __name__ == '__main__':
    app.run(debug=True)
