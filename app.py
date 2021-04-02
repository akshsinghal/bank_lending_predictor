import flask
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import sys

#load models at top of app to load into memory only one time
with open('models/rf.pickle', 'rb') as f:
    clf_individual = pickle.load(f)

ss = StandardScaler()

df_macro_mean  = pd.read_csv('data/Mean.csv', index_col=0, dtype=np.float64)

df_macro_std = pd.read_csv('data/std.csv', index_col=0, dtype=np.float64)


app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    print("hello")
    return (flask.render_template('index.html'))


@app.route('/report')
def report():
    return (flask.render_template('report.html'))



@app.route("/Individual", methods=['GET', 'POST'])
def Individual():
    sys.stdout.flush()
    if flask.request.method == 'GET':
        return (flask.render_template('Individual.html'))

    if flask.request.method =='POST':


        Age = flask.request.form['Age']
        print(Age)

        Income = float(flask.request.form['Monthly Net Income'])
        CreditScore = float(flask.request.form['Credit Score'])
        HouseholdSize = float(flask.request.form['Household Size'])
        State = (flask.request.form['State'])
        MedianHomeValue = float(flask.request.form['Median Home Value'])
        MedianHouseholdIncome = float(flask.request.form['Median Household Income'])
        Debt = float(flask.request.form['Debt'])
        LoanTerm= float(flask.request.form['term'])
        InterestRate = float(flask.request.form['Interest Rate'])
        CreditIncidents	 = float(flask.request.form['Credit Incidents'])
        HomeValue = float(flask.request.form['Home Value'])
        LoanAmount = float(flask.request.form['Loan Amount'])
        ProductType = (flask.request.form['Product Type'])

        product_dict = {'Adjustable_rate': 0, 'Fixed_rate': 1, 'Government_insured': 2, 'Jumbo': 3}
        state_dict = {'AL': 0,
 'AR': 1,
 'AZ': 2,
 'CA': 3,
 'CO': 4,
 'CT': 5,
 'FL': 6,
 'GA': 7,
 'HI': 8,
 'IA': 9,
 'ID': 10,
 'IL': 11,
 'IN': 12,
 'KS': 13,
 'KY': 14,
 'LA': 15,
 'MA': 16,
 'MD': 17,
 'ME': 18,
 'MI': 19,
 'MN': 20,
 'MO': 21,
 'MS': 22,
 'NC': 23,
 'NH': 24,
 'NJ': 25,
 'NM': 26,
 'NV': 27,
 'NY': 28,
 'OH': 29,
 'OK': 30,
 'OR': 31,
 'PA': 32,
 'RI': 33,
 'SC': 34,
 'TN': 35,
 'TX': 36,
 'UT': 37,
 'VA': 38,
 'VT': 39,
 'WA': 40,
 'WI': 41,
 'WV': 42}
        temp = pd.DataFrame(index=[1])
        temp['Age']=Age
        temp['Income']=Income
        temp['CreditScore']= CreditScore
        temp['HouseholdSize']=HouseholdSize
        temp['State']= state_dict[State]
        temp['MedianHomeValue']= MedianHomeValue
        temp['MedianHouseholdIncome']=MedianHouseholdIncome
        temp['Debt'] = Debt
        temp['LoanTerm']=LoanTerm
        temp['InterestRate']=InterestRate
        temp['CreditIncidents']=CreditIncidents
        temp['HomeValue'] = HomeValue
        temp['LoanAmount']=LoanAmount
        temp['ProductType']= product_dict[ProductType]

        #create original output dict
        output_dict= dict()
        output_dict['Provided Annual Income'] = Income
        output_dict['Provided Credit Score'] = CreditScore
        #output_dict['Predicted Interest Rate'] = int_rate * 100 #revert back to percentage
        #output_dict['Estimated Installment Amount']=installment
        #output_dict['Number of Payments'] = 36 if term==1 else 60
        #output_dict['Sub Grade']= sub_grade_to_char[35-int(sub_grade)]
        #output_dict['Loan Amount']=loan_amnt

        #create deep copy
        scale = temp.copy()
        for feat in df_macro_mean.columns:
            scale[feat] = (scale[feat] - df_macro_mean[feat].values[0]) / df_macro_std[feat].values[0]


        #make prediction
        pred = clf_individual.predict(scale)

        if pred==1:
            res = f'Congratulations! Approved!'
        else:
            res = f'Sorry, we can\'t provide you with a loan'



        #render form again and add prediction
        return flask.render_template('Individual.html', original_input=output_dict, result=res)



if __name__ == '__main__':
    app.run(debug=True)
