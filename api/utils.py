import pandas as pd 
import os, logging, datetime

def current_time():
    return datetime.datetime.now()
    
def save_csv(df, filename):
    df.to_csv(os.path.join("./",filename), encoding="big5", index=False) 
    logging.info("save " + filename + "\t" + str(current_time()))

def process_10swallow(data):
    # # save 10 swallows data to csv 
    data = data.dict()
    id = data["ID"]
    doctor_num = str(data["doctor"])
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
    print(df)
    save_csv(df, id+"_"+doctor_num + ".csv")

    
