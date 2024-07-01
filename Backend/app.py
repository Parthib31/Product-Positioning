from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

model = pickle.load(open("new_model.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onsubmit', methods=['POST'])
def on_submit():
    if request.method == 'POST':
        Price = float(request.form['Price'])
        CompetitorPrice=float(request.form["Competitor's Price"])
        Promotion_Yes= request.form['Promotion']
        if(Promotion_Yes == "Yes"):
            Promotion_Yes = 1
        else:
            Promotion_Yes = 0

        Foot_Traffic_Low = request.form['Foot Traffic']
        if(Foot_Traffic_Low == 'Low'):
            Foot_Traffic_Low = 1
            Foot_Traffic_Medium = 0
        
        if(Foot_Traffic_Low == 'Medium'):
            Foot_Traffic_Low=0
            Foot_Traffic_Medium = 1
            
        else:
            Foot_Traffic_Low=0
            Foot_Traffic_Medium = 0            

        
        Consumer_Demographics_Families = request.form['Consumer Demographics']
        if(Consumer_Demographics_Families == "Families"):
            Consumer_Demographics_Families = 1
            Consumer_Demographics_Seniors = 0
            Consumer_Demographics_Young_adults = 0

        if(Consumer_Demographics_Families == "Seniors"):
            Consumer_Demographics_Families = 0
            Consumer_Demographics_Seniors = 1
            Consumer_Demographics_Young_adults = 0
        
        if(Consumer_Demographics_Families == "Young adults"):
            Consumer_Demographics_Families = 0
            Consumer_Demographics_Seniors = 0
            Consumer_Demographics_Young_adults = 1
        
        else:
            Consumer_Demographics_Families = 0
            Consumer_Demographics_Seniors = 0
            Consumer_Demographics_Young_adults = 0
        
        	
        Product_Category_Electronics =request.form['Product Category']

        if(Product_Category_Electronics == "Electronics"):
            Product_Category_Electronics = 1
            Product_Category_Food = 0
        
        if(Product_Category_Electronics == "Food"):
            Product_Category_Electronics = 0
            Product_Category_Food = 1
        
        else:
            Product_Category_Electronics = 0
            Product_Category_Food = 0

        seasonal_yes = request.form["Seasonal"]
        if(seasonal_yes == 'Yes'):
            seasonal_yes = 1
        else:
            seasonal_yes = 0

        sales_volume = float(request.form["Sales Volume"])

        prediction=model.predict([[Price, CompetitorPrice, sales_volume, Promotion_Yes, Foot_Traffic_Low, Foot_Traffic_Medium,Consumer_Demographics_Families, Consumer_Demographics_Seniors, Consumer_Demographics_Young_adults, Product_Category_Electronics, Product_Category_Food, seasonal_yes]])

        pred = prediction[0]
        print(prediction)
        if pred  == 0:
            output = "Aisle"
        elif pred  == 1:
            output = "End-Cap"
        else:
            output = "Front of Store"

        return render_template('index.html',prediction_text="The product position is {}".format(output))
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
