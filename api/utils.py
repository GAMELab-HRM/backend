import pandas as pd 
import numpy as np
import json, os, logging, datetime, shutil, pytz, pickle

# 這個function會回傳需要存入database的數值
def parsing_csv(df):
    df['檢查流程'] = df['檢查流程'].fillna('None')
    column_names = df.columns
    swallow_names = ["Wet swallow"+str(i+1) for i in range(10)]
    mrs_names = ["MRS"+str(i+1) for i in range(5)]
    sensor_num = 0 

    for i in column_names:
        if i[1] == "P":
            sensor_num+=1

    sensors = [" P"+str(i+1) for i in range(sensor_num)]
    ans = list(np.where(df['檢查流程']!='None')[0])

    swallow_index = []
    mrs_index = []
    for i in range(len(ans)):
        test_name = df.iloc[ans[i]]['檢查流程']
        if i == len(ans)-1:
            next_name = ""
        else:
            next_name = df.iloc[ans[i+1]]['檢查流程']

        if test_name in swallow_names:
            swallow_index.append(ans[i])
            if "Wet swallow" not in next_name:
                swallow_index.append(ans[i+1])

        if test_name in mrs_names:
            mrs_index.append(ans[i])
            if "MRS" not in next_name:
                if i+1<len(ans):
                    mrs_index.append(ans[i+1])
                else:
                    mrs_index.append(len(df)-1)
    mrs_list = [] # 存放3~5次mrs的raw data 
    for i in range(len(mrs_index)-1):
        mrs_i = df[mrs_index[i]:mrs_index[i+1]][sensors].astype(np.float32).values
        mrs_i = np.transpose(mrs_i)
        mrs_i = mrs_i.tolist()
        mrs_list.append(mrs_i)

    swallow_list = [] # 存放10個swallow的raw data
    for i in range(len(swallow_index)-1):
        swallow_i = df[swallow_index[i]:swallow_index[i+1]][sensors].astype(np.float32).values
        swallow_i = np.transpose(swallow_i)
        swallow_i = swallow_i.tolist()
        swallow_list.append(swallow_i)
    #print(swallow_list[0])

    return swallow_list, mrs_list, sensor_num


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
    retv = []
    temp = np.transpose(all_swallows_data)
    temp = temp.tolist()
    # for i in range(len(temp)-1,-1,-1):
    #     retv.append(temp[i])
    
    return json.dumps(temp), swallow_index[:-1], sensor_num

def current_time():
    tw = pytz.timezone("Asia/Taipei")
    return " | " + str(tw.localize(datetime.datetime.now()))
    
def check_folder_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)
        logging.info("Create folder: " + path)

def save_file(path, filename, df):
    check_folder_exist(path)
    
    # save file 
    # with open(path + files.filename, "wb+") as file_object:
    #     shutil.copyfileobj(files.file, file_object)
    df.to_csv(path+filename, index=False, encoding='big5')
    logging.info("save " + filename + current_time())
    

def backup_csv(df, path, filename):
    # check csv folder exist?
    check_folder_exist(path)
    df.to_csv(path+filename, encoding="big5", index=False) 
    logging.info("save " + filename + "\t" + str(current_time()))


    
