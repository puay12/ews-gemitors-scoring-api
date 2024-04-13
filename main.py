from flask import Flask, app, request
import scoring
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def route():
    return  {'status': True, 'message': 'This is a EWS service by Putri Ayu'}, 200

@app.route('/getEWSScore', methods=['GET', 'POST'])
def get_EWS_Score():
    request_data = {
        "heart_rate": float(request.form['heart_rate']),
        'systolic_blood_pressure': float(request.form['systolic_blood_pressure']),
        'diastolic_blood_pressure': float(request.form['diastolic_blood_pressure']),
        'respiratory_rate': float(request.form['respiratory_rate']),
        'temperature': float(request.form['temperature']),
        'spo2': float(request.form['spo2'])
    }

    data = scoring.calculate_ews_score(request_data)
    total = scoring.calculate_total_score(data)
    data.update({'ews_score':total})
    
    for key,value in data.items():
        data[key] = str(value)

    return {'message': 'Berhasil menghitung skor EWS pasien!', 'data': data}, 200

if __name__ == '__main__':
    app.run()
