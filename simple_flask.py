from flask import Flask,request, jsonify
import pandas as pd
import json


app = Flask(__name__)


data = pd.read_csv('staff_data.csv')

@app.route('/api/data',methods=['GET'])
def get_data():

    return jsonify(data.to_dict(orient='records'))

@app.route('/years_of_experience',methods=['POST'])
def get_years_of_experience():

    params=json.loads(request.get_data().decode())

    print(params)

    name=params['Name']

    department=params['Department']


    print('department:',department)
    print('name:',name)

    years_of_exp =list(data.loc[(data['Department']==department)&
                                (data['Name']==name),'Years_of_Experience'])[0]

    return jsonify({"years of experience":years_of_exp})


@app.route('/candidates',methods=['POST'])
def candidates_by_yoe():

    params=json.loads(request.get_data().decode())

    print(params)

    yoe=int(params['years_of_experience'])

    print('years of experience:',yoe)

    op=data.loc[data['Years_of_Experience']==yoe].to_dict(orient='records')   

    return jsonify(op)



if __name__=="__main__":

    app.run(debug=True)
