import pandas as pd 
import numpy as np
import json, os, logging, datetime, shutil, pytz, pickle

# for 10 wet swallows 
def preprocess_csv(df):
    df['檢查流程'] = df['檢查流程'].fillna('None')
    column_names = df.columns
    swallow_names = ["Wet swallow"+str(i+1) for i in range(10)]
    sensor_num = 0 
    for i in column_names:
        if i[1] == "P":
            sensor_num+=1
    sensors = [" P"+str(i+1) for i in range(sensor_num)]
    ans = list(np.where(df['檢查流程']!='None')[0])

    swallow_index = []
    swallow_range = []

    for i in range(len(ans)):
        test_name = df.iloc[ans[i]]['檢查流程']
        if 'Wet swallow10' == test_name:
            swallow_index.append(ans[i])
            swallow_index.append(ans[i+1])
            continue

        if test_name in swallow_names:
            swallow_index.append(ans[i])
        
    all_swallows_data = df[swallow_index[0]:swallow_index[10]][sensors].values
    """
    TODO:
        這邊的swallow_index要轉換成以0開始
    """
    return json.dumps(all_swallows_data.tolist()), swallow_index[:-1], sensor_num

def current_time():
    tw = pytz.timezone("Asia/Taipei")
    return " | " + str(tw.localize(datetime.datetime.now()))
    
def check_folder_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)
        logging.info("Create folder: " + path)

def save_file(path, files):
    check_folder_exist(path)
    # save file 
    with open(path + files.filename, "wb+") as file_object:
        shutil.copyfileobj(files.file, file_object)
    logging.info("save " + files.filename + current_time())
    

def backup_csv(df, path, filename):
    # check csv folder exist?
    check_folder_exist(path)
    df.to_csv(path+filename, encoding="big5", index=False) 
    logging.info("save " + filename + "\t" + str(current_time()))

def process_10swallow(data):
    # # save 10 swallows data to csv 
    data = data.dict()
    id = data["ID"]
    doctor_num = str(data["doctor"])
    cc_result = str(data["cc_result"])
    columns_name = [
        "ID",
        "V",
        "P",
        "swallow_type",
        "IRP40",
        "DCI",
        "DL",
        "cc_result"
    ]

    columns_name_aug = ["ID"]
    csv_data = [data["ID"]]

    for i in range(1, len(columns_name)-1):
        temp = columns_name[i]
        for j in range(len(data[temp])):
            csv_data.append(data[temp][j])
        for j in range(10):
            columns_name_aug.append(columns_name[i]+"_"+str(j+1))
    columns_name_aug.append("cc_result")
    csv_data.append(data["cc_result"])
    df = pd.DataFrame([csv_data], columns=columns_name_aug)
    filename = id+"_"+cc_result+"_"+doctor_num+"_10swallows.csv"
    backup_csv(df, "./data/csv_backup/", filename)

    
