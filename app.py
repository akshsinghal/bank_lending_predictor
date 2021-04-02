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

        #get input

        #ask for first 2 digits of zip code as integer
        code = int(flask.request.form['code'])
        #fico score as integer
        fico_avg_score = int(flask.request.form['fico_avg_score'])
        #loan amount as integer
        loan_amnt = float(flask.request.form['loan_amnt'])
        #term as integer: 36 or 60
        term = int(flask.request.form['term'])
        #debt to income as float
        dti = float(flask.request.form['dti'])
        #home ownership as string
        home_ownership = flask.request.form['home_ownership']
        #number or mortgage accounts as integer
        mort_acc = int(flask.request.form['mort_acc'])
        #annual income as float
        annual_inc = float(flask.request.form['annual_inc'])
        #number of open accounts as integer
        open_acc = int(flask.request.form['open_acc'])
        #verification status as 0, 1, 2
        verification_status = int(flask.request.form['verification_status'])
        #revolving utilization as float
        revol_util = float(flask.request.form['revol_util'])
        #The total number of credit lines currently in the borrower's credit file
        total_acc = int(flask.request.form['total_acc'])
        #time since first credit line in months
        er_credit_open_date = pd.to_datetime(flask.request.form['er_credit_open_date'])
        issue_d = pd.to_datetime("today")
        credit_hist = issue_d - er_credit_open_date
        credit_line_ratio=open_acc/total_acc
        balance_annual_inc=loan_amnt/annual_inc
        #calculate grade from FICO
        sub_grade = knn.predict(np.reshape([fico_avg_score], (1,-1)))[0]
        #calculate grade
        grade = round(sub_grade/5) + 1
        #get interest rate
        apr_row = df_fico_apr[df_fico_apr['grade_num']==sub_grade]




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
