import pandas as pd

def castData(row):
    data = []
    
    new_row = row.drop(columns='Vital Sign')
    
    for col in new_row:
        obj = new_row[col].iloc[0]
        
        if type(obj) == str:
            casted = obj.split(',')
            casted = [float(x) for x in casted]
        else:
            casted = float(obj)
        
        data.append(casted)
    
    return data

def calculate_ews_score(request_data):
    final_scores = {
        'heart_rate': 0,
        'systolic_blood_pressure': 0,
        'diastolic_blood_pressure': 0,
        'respiratory_rate': 0,
        'temperature': 0,
        'spo2': 0
    }

    ews_table = pd.read_excel('Generated_EWSTable.xlsx')

    for key,value in request_data.items():
        match(key):
            case 'heart_rate':
                row = ews_table[ews_table["Vital Sign"]=="Heart Rate"]
            case 'systolic_blood_pressure':
                row = ews_table[ews_table["Vital Sign"]=="Systolic Blood Pressure"]
            case 'diastolic_blood_pressure':
                row = ews_table[ews_table["Vital Sign"]=="Diastolic Blood Pressure"]
            case 'respiratory_rate':
                row = ews_table[ews_table["Vital Sign"]=="Respiratory Rate"]
            case 'temperature':
                row = ews_table[ews_table["Vital Sign"]=="Temperature"]
            case 'spo2':
                row = ews_table[ews_table["Vital Sign"]=="SPO2"]
        
        data = castData(row)
        value = float(value)
        
        for i,item in enumerate(data):
            if item != 0.0:
                if type(item) == float:
                    if ((value >= item) & (i == (len(data)-1))) | ((value <= item) & (i == 0)):
                        score = 3
                else:
                    next_val = data[i+1]
                    
                    if i < 5:
                        next_val = next_val[0]
                        
                    if ((value >= item[1]) & (value <= next_val)) | ((value >= item[0]) & (value <= item[1])):
                        match(i):
                                case 1:
                                    score = 2
                                case 2:
                                    score = 1
                                case 3:
                                    score = 0
                                case 4:
                                    score = 1
                                case 5:
                                    score = 2
        
        final_scores.update({key:score})
    
    return final_scores


def calculate_total_score(scores):
    total = 0
    
    for score in scores.values():
        total += score

    return total