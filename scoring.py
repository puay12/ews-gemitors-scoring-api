import pandas as pd

def castData(row):
    data = []
    
    new_row = row.drop(columns='vital_sign')
    
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
    final_scores = {}

    ews_table = pd.read_excel('Generated_EWSTable.xlsx')

    for key,value in request_data.items():
        match(key):
            case 'heart_rate':
                row = ews_table[ews_table["vital_sign"]=="Heart Rate"]
                final_key = 'heart_score'
            case 'systolic_blood_pressure':
                row = ews_table[ews_table["vital_sign"]=="Systolic Blood Pressure"]
                final_key = 'sys_score'
            case 'diastolic_blood_pressure':
                row = ews_table[ews_table["vital_sign"]=="Diastolic Blood Pressure"]
                final_key = 'dias_score'
            case 'respiratory_rate':
                row = ews_table[ews_table["vital_sign"]=="Respiratory Rate"]
                final_key = 'respiratory_score'
            case 'temperature':
                row = ews_table[ews_table["vital_sign"]=="Temperature"]
                final_key = 'temp_score'
            case 'spo2':
                row = ews_table[ews_table["vital_sign"]=="SPO2"]
                final_key = 'spo2_score'
        
        data = castData(row)
        value = float(value)
        
        for i,item in enumerate(data):
            if item != 0.0:
                if type(item) == float:
                    if (((value >= item) & (i == (len(data)-1))) | ((value <= item) & (i == 0))):
                        score = 3
                else:
                    next_val = data[i+1]
                    
                    if i < 5:
                        next_val = next_val[0]
                        
                    if ((value >= item[1]) & (value <= next_val)) | ((value >= item[0]) & (value <= item[1])):
                        score = match_score(i)
                    else :
                        prev_val = data[i-1]
                        
                        if((prev_val == 0.0) & (i > 0)):
                            score = match_score(i)
        
        final_scores.update({final_key:score})
    
    return final_scores


def calculate_total_score(scores):
    total = 0
    
    for score in scores.values():
        total += score

    return total

def match_score(i):
    match(i):
        case 1:
            return 2
        case 2:
            return 1
        case 3:
            return 0
        case 4:
            return 1
        case 5:
            return 2