import pandas as pd 
import numpy as np
import json, os, logging, datetime, shutil, pytz, pickle
from typing import Tuple, List

# 計算swallow type
def compute_type(vigor: str, pattern: str) -> str:
    vigor = vigor.replace(" ","")
    pattern = pattern.replace(" ","")
    if pattern == "Intact" or pattern == "Failed":
        return vigor 
    if pattern == "Fragmented" or pattern == "Premature":
        return pattern

# sensor mapping 
def get_sensor_num(catheter_type: int) -> int: 
    if catheter_type == 1: # K103659-E-1545-D
        return [" P" + str(i+1) for i in range(36)]
    elif catheter_type == 2: # K83259-E-1263-D
        return [" P" + str(i+1) for i in range(32)]
    elif catheter_type == 3: # CE4-1083
        return [" P" + str(i+1) for i in range(22)]
    elif catheter_type == 4: # CE4-0062
        return [" P" + str(i+1) for i in range(22)]
    elif catheter_type == 5: # CE4-0037
        return [" P" + str(i+1) for i in range(20)]
    elif catheter_type == 6:
        return [" P" + str(i+1) for i in range(36)] 
    
# 得到哪幾個swallow是有效的 (有些swallow是失敗的)
def get_ws_names(df: pd.DataFrame,) -> Tuple[List, List, List, int]:
    label_df = df[["ws_10_vigor", "ws_10_pattern", "ws_10_dci", "ws_10_irp40", "ws_10_dl", "ws_10_large_break"]]
    label_df = label_df.fillna("None")
    vigors = [x for x in label_df["ws_10_vigor"].values if x!= "None"] 
    ws_num = len(vigors)
    patterns = (label_df["ws_10_pattern"][:ws_num].values).tolist()
    dcis = (label_df["ws_10_dci"][:ws_num].values).tolist()
    irps = (label_df["ws_10_irp40"][:ws_num].values).tolist()
    dls = (label_df["ws_10_dl"][:ws_num].values).tolist()
    large_breaks = (label_df["ws_10_large_break"][:ws_num].values).tolist()
    failed_index = []
    # find failed swallow 
    for index in range(len(vigors)):
        if vigors[index] == "無數據":
            failed_index.append(index)
    catheter_type = int(df["catheter_type"].values[0])
    return  vigors, patterns, dcis, irps, dls, large_breaks, failed_index, catheter_type

def get_ws10_new(df: pd.DataFrame, ws_num: int, failed_index: List, vigors: List, patterns:List, catheter_type: int,) -> Tuple[List, List, List]:
    """
        ws_num: 有些病人不只有10個swallow (有幾次可能是無效的)
    """
    df['檢查流程'] = df['檢查流程'].fillna('None')
    swallow_index, swallow_list, swallow_types = [], [], []
    sensors = get_sensor_num(catheter_type)
    # get wet swallow index 
    for index in range(ws_num):
        if index in failed_index:
            continue
        vigor = vigors[index]
        pattern = patterns[index]
        target_index = int(np.where(df["檢查流程"]=="Wet Swallow" + str(index+1))[0])
        swallow_index.append(target_index)
        swallow_types.append(compute_type(vigor, pattern))
        swallow_i = df[target_index-80:target_index+440][sensors].astype(np.float32).values # 2022/01/29 只取12秒 (改看看，看效能會不會變好)
        swallow_i = np.transpose(swallow_i)
        swallow_i = swallow_i.tolist()
        swallow_list.append(swallow_i)
    return swallow_list, swallow_types, [i for i in range(ws_num) if i not in failed_index], swallow_index

def get_new(df: pd.DataFrame, catheter_type: int):
    df['檢查流程'] = df['檢查流程'].fillna('None')
    ans = list(np.where(df['檢查流程']!='None')[0])
    sensors = get_sensor_num(catheter_type)
    all_data = df[:][sensors].astype(np.float32).values 
    all_data = (np.transpose(all_data)).tolist()
    mrs_names = ["MRS"+str(i+1) for i in range(10)]
    hh_names = ["Landmark"]
    mrs_index, hh_index = [], []
    mrs_list, hh_list = [], []
    for i in range(len(ans)):
        test_name = df.iloc[ans[i]]['檢查流程']
        if test_name in mrs_names:
            mrs_index.append(ans[i].item())
        
        if test_name in hh_names:
            hh_index.append(ans[i].item())
    print(mrs_index)
    for i in range(len(mrs_index)):
        #mrs_i = df[mrs_index[i]-80:mrs_index[i]+520][sensors].astype(np.float32).values # 2022/0205/ mrs可能要往後抓一點
        mrs_i = df[mrs_index[i]-80:mrs_index[i]+600][sensors].astype(np.float32).values # 2022/0213/ 
        mrs_i = np.transpose(mrs_i)
        mrs_i = mrs_i.tolist()
        mrs_list.append(mrs_i)
        
    for i in range(len(hh_index)):
        hh_i = df[hh_index[i]:hh_index[i]+480][sensors].astype(np.float32).values 
        hh_i = np.transpose(hh_i)
        hh_i = hh_i.tolist()
        hh_list.append(hh_i)
    return mrs_list, mrs_index, hh_list, hh_index, all_data

def parsing_csv_new(df: pd.DataFrame):
    vigors, patterns, dcis, irps, dls, large_breaks, failed_index, catheter_type = get_ws_names(df)
    swallow_list, swallow_types, failed_index, swallow_index = get_ws10_new(df, len(vigors), failed_index, vigors, patterns, catheter_type)
    mrs_list, mrs_index, hh_list, hh_index, all_data = get_new(df, catheter_type)
    return swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, catheter_type, all_data

# 這個function會回傳需要存入database的數值
def parsing_csv(df: pd.DataFrame) -> Tuple[List, List, List, int]:
    df['檢查流程'] = df['檢查流程'].fillna('None')
    column_names = df.columns
    hh_names = ["Landmark"]
    swallow_names = ["Wet swallow"+str(i+1) for i in range(10)]
    mrs_names = ["MRS"+str(i+1) for i in range(5)]
    sensor_num = 0 

    for i in column_names:
        if i[1] == "P":
            sensor_num+=1

    sensors = [" P"+str(i+1) for i in range(sensor_num)]
    all_data = df[:][sensors].astype(np.float32).values 
    all_data = (np.transpose(all_data)).tolist()
    
    ans = list(np.where(df['檢查流程']!='None')[0])

    hh_index, swallow_index, mrs_index = [], [], []
    hh_list, swallow_list, mrs_list = [], [], []
    for i in range(len(ans)):
        test_name = df.iloc[ans[i]]['檢查流程']
        if i == len(ans)-1:
            next_name = ""
        else:
            next_name = df.iloc[ans[i+1]]['檢查流程']
        if test_name in hh_names:
            hh_index.append(ans[i])
            
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
    
    for i in range(len(hh_index)):
        hh_i = df[hh_index[i]:hh_index[i]+480][sensors].astype(np.float32).values 
        hh_i = np.transpose(hh_i)
        hh_i = hh_i.tolist()
        hh_list.append(hh_i)
    
    for i in range(len(mrs_index)-1):
        #mrs_i = df[mrs_index[i]:mrs_index[i+1]][sensors].astype(np.float32).values #原本的作法
        mrs_i = df[mrs_index[i]-80:mrs_index[i]+520][sensors].astype(np.float32).values # 2022/0205/ mrs可能要往後抓一點
        mrs_i = np.transpose(mrs_i)
        mrs_i = mrs_i.tolist()
        mrs_list.append(mrs_i)

    for i in range(len(swallow_index)-1):
        #swallow_i = df[swallow_index[i]:swallow_index[i+1]][sensors].astype(np.float32).values #原本的作法
        swallow_i = df[swallow_index[i]-80:swallow_index[i]+440][sensors].astype(np.float32).values # 2021/12/07 更新,會往前多抓4秒,往後抓22秒,一個swallow共26秒
        swallow_i = np.transpose(swallow_i)
        swallow_i = swallow_i.tolist()
        swallow_list.append(swallow_i)
    #print(swallow_list[0])
    print(len(swallow_list), len(mrs_list), len(hh_list))
    return swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, -1, all_data


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
    
    return json.dumps(temp), swallow_index[:-1], sensor_num

def current_time() -> str:
    tw = pytz.timezone("Asia/Taipei")
    return " | " + str(tw.localize(datetime.datetime.now()))
    
def check_folder_exist(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)
        logging.info("Create folder: " + path)

def save_file(path: str, filename: str, df: pd.DataFrame) -> None:
    check_folder_exist(path)
    df.to_csv(path+filename, index=False, encoding='big5')
    logging.info("save " + filename + current_time())
    

def backup_csv(df: pd.DataFrame, path: str, filename: str) -> None:
    check_folder_exist(path)
    df.to_csv(path+filename, encoding="big5", index=False) 
    logging.info("save " + filename + "\t" + str(current_time()))


    
