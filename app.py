import os
from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        # Validation
        if request.form['credit'] == '-- select Credit_History --':
            return render_template("prediction.html", prediction_text="Please select a valid Credit History")

        # Get inputs
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # Encoding

        # gender
        male = 1 if gender == "Male" else 0

        # married
        married_yes = 1 if married == "Yes" else 0

        # dependents
        dependents_1 = 1 if dependents == '1' else 0
        dependents_2 = 1 if dependents == '2' else 0
        dependents_3 = 1 if dependents == '3+' else 0

        # education
        not_graduate = 1 if education == "Not Graduate" else 0

        # employed
        employed_yes = 1 if employed == "Yes" else 0

        # property area
        semiurban = 1 if area == "Semiurban" else 0
        urban = 1 if area == "Urban" else 0

        # Log transformations
        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        # Prediction
        prediction = model.predict([[
            credit,
            ApplicantIncomelog,
            LoanAmountlog,
            Loan_Amount_Termlog,
            totalincomelog,
            male,
            married_yes,
            dependents_1,
            dependents_2,
            dependents_3,
            not_graduate,
            employed_yes,
            semiurban,
            urban
        ]])

        # 🔥 FIX: extract value from array
        prediction = prediction[0]

        # Convert result
        if prediction == "N":
            result = "Rejected"
        else:
            result = "Approved"

        return render_template("prediction.html", prediction_text=f"Your loan is {result}")

    return render_template("prediction.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)