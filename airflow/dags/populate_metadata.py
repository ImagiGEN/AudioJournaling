from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kaggle.api.kaggle_api_extended import KaggleApi
from airflow.models.baseoperator import chain
from dotenv import load_dotenv
import os
from utils.db_utils import engine
import pandas as pd


# Load variables from .env file
load_dotenv()

kaggle_api = KaggleApi()
kaggle_api.authenticate()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 6),
    'retries': 1,
}

dag = DAG('compute_metadata', default_args=default_args, schedule_interval=None)

def fetch_from_kaggle(dataset_name, download_path):
    api = KaggleApi()
    api.authenticate()
    data_name = dataset_name.split(',')
    for dset in data_name:
        print("dataset name")
        print(dset)
        api.dataset_download_files(dset, path=download_path, unzip=True)
    print("Data fetched from Kaggle.")

def compute_metadata(download_path):
    print(os.listdir(download_path))
    print(download_path)
    df1 = explore_RAV(download_path)
    df2 = explore_SAVEE(download_path)
    df3 = explore_TESS(download_path)
    df4 = explore_CREMAD(download_path)
    final_df = pd.concat([df1, df2, df3, df4])
    print(final_df.head())
    print(final_df.shape)
    save_to_sql(final_df)

def save_to_sql(df):
    df.to_sql("audio_data_metadata", engine, if_exists='replace')

def explore_SAVEE(path):
    SAVEE = "ALL/"
    data_dir = os.path.join(path, SAVEE)
    dir_list = os.listdir(data_dir)

    # parse the filename to get the emotions
    emotion=[]
    gender = []
    path = []
    for i in dir_list:
        if i[-8:-6]=='_a':
            emotion.append('angry')
        elif i[-8:-6]=='_d':
            emotion.append('disgust')
        elif i[-8:-6]=='_f':
            emotion.append('fear')
        elif i[-8:-6]=='_h':
            emotion.append('happy')
        elif i[-8:-6]=='_n':
            emotion.append('neutral')
        elif i[-8:-6]=='sa':
            emotion.append('sad')
        elif i[-8:-6]=='su':
            emotion.append('surprise')
        else:
            emotion.append('error') 
        gender.append('male')
        path.append(data_dir + i)
        
    # Now check out the label count distribution 
    SAVEE_df = pd.DataFrame(emotion, columns = ['emotion'])
    SAVEE_df = pd.concat([pd.DataFrame(gender, columns=['gender']),SAVEE_df],axis=1)
    SAVEE_df['source'] = 'SAVEE'
    SAVEE_df = pd.concat([SAVEE_df, pd.DataFrame(path, columns = ['path'])], axis = 1)
    return SAVEE_df

def explore_CREMAD(path):
    CREMA = "AudioWAV/"
    data_dir = os.path.join(path, CREMA)
    dir_list = os.listdir(data_dir)
    dir_list.sort()
    gender = []
    emotion = []
    path = []
    female = [1002,1003,1004,1006,1007,1008,1009,1010,1012,1013,1018,1020,1021,1024,1025,1028,1029,1030,1037,1043,1046,1047,1049,
            1052,1053,1054,1055,1056,1058,1060,1061,1063,1072,1073,1074,1075,1076,1078,1079,1082,1084,1089,1091]

    for i in dir_list: 
        part = i.split('_')
        if int(part[0]) in female:
            temp = 'female'
        else:
            temp = 'male'
        gender.append(temp)
        if part[2] == 'SAD':
            emotion.append('sad')
        elif part[2] == 'ANG':
            emotion.append('angry')
        elif part[2] == 'DIS':
            emotion.append('disgust')
        elif part[2] == 'FEA':
            emotion.append('fear')
        elif part[2] == 'HAP':
            emotion.append('happy')
        elif part[2] == 'NEU':
            emotion.append('neutral')
        else:
            emotion.append('Unknown')
        path.append(data_dir + i)
        
    CREMA_df = pd.DataFrame(emotion, columns = ['emotion'])
    CREMA_df = pd.concat([pd.DataFrame(gender, columns=['gender']),CREMA_df],axis=1)
    CREMA_df['source'] = 'CREMA'
    CREMA_df = pd.concat([CREMA_df,pd.DataFrame(path, columns = ['path'])],axis=1)
    # CREMA_df.labels.value_counts()
    return CREMA_df

def explore_TESS(path):
    TESS = "TESS Toronto emotional speech set data/"
    data_dir = os.path.join(path, TESS)
    dir_list = os.listdir(data_dir)
    dir_list.sort()
    path = []
    emotion = []
    gender = []

    for i in dir_list:
        fname = os.listdir(data_dir + i)
        for f in fname:
            if i == 'OAF_angry' or i == 'YAF_angry':
                emotion.append('angry')
            elif i == 'OAF_disgust' or i == 'YAF_disgust':
                emotion.append('disgust')
            elif i == 'OAF_Fear' or i == 'YAF_fear':
                emotion.append('fear')
            elif i == 'OAF_happy' or i == 'YAF_happy':
                emotion.append('happy')
            elif i == 'OAF_neutral' or i == 'YAF_neutral':
                emotion.append('neutral')                                
            elif i == 'OAF_Pleasant_surprise' or i == 'YAF_pleasant_surprised':
                emotion.append('surprise')               
            elif i == 'OAF_Sad' or i == 'YAF_sad':
                emotion.append('sad')
            else:
                emotion.append('Unknown')
            gender.append('female')
            path.append(data_dir + i + "/" + f)

    TESS_df = pd.DataFrame(emotion, columns = ['emotion'])
    TESS_df = pd.concat([pd.DataFrame(gender, columns=['gender']),TESS_df],axis=1)
    TESS_df['source'] = 'TESS'
    TESS_df = pd.concat([TESS_df,pd.DataFrame(path, columns = ['path'])],axis=1)
    return TESS_df

def explore_RAV(path):
    RAV = "audio_speech_actors_01-24/"
    data_dir = os.path.join(path, RAV)
    dir_list = os.listdir(data_dir)
    dir_list.sort()

    emotion = []
    gender = []
    path = []
    for i in dir_list:
        fname = os.listdir(data_dir + i)
        for f in fname:
            part = f.split('.')[0].split('-')
            emotion.append(int(part[2]))
            temp = int(part[6])
            if temp%2 == 0:
                temp = "female"
            else:
                temp = "male"
            gender.append(temp)
            path.append(data_dir + i + '/' + f)

            
    RAV_df = pd.DataFrame(emotion)
    RAV_df = RAV_df.replace({1:'neutral', 2:'neutral', 3:'happy', 4:'sad', 5:'angry', 6:'fear', 7:'disgust', 8:'surprise'})
    RAV_df = pd.concat([pd.DataFrame(gender),RAV_df],axis=1)
    RAV_df.columns = ['gender','emotion']
    RAV_df['source'] = 'RAVDESS'
    RAV_df = pd.concat([RAV_df,pd.DataFrame(path, columns = ['path'])],axis=1)
    return RAV_df

with dag:
    fetch_from_kaggle_task = PythonOperator(
        task_id='fetch_from_kaggle',
        python_callable=fetch_from_kaggle,
        op_kwargs={
            'dataset_name': os.getenv("KAGGLE_DATASET_NAME"),
            'download_path': os.getenv("DATA_DOWNLOAD_PATH"),
        },
    )
    compute_metadata_task = PythonOperator(
        task_id='compute_metadata',
        python_callable=compute_metadata,
        op_kwargs={
            'download_path': os.getenv("DATA_DOWNLOAD_PATH"),
        },
    )
    chain(fetch_from_kaggle_task, compute_metadata_task)
