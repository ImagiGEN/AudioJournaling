## Technical stack
![Codelabs](https://img.shields.io/badge/Codelabs-violet?style=for-the-badge)
![GCP provider](https://img.shields.io/badge/GCP-orange?style=for-the-badge&logo=google-cloud&color=orange)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

## Link to the Live Applications
* [Streamlit](https://demo.ashrithag.me)
* [Codelabs](https://codelabs-preview.appspot.com/?file_id=1E2Z6QsyAEtmAuYTbtrClYIojHb8P_ISyPxjJWQZxXi8#0)


# SoundJot
The cutting-edge audio journaling application designed to preserve your thoughts, 
emotions, and cherished moments through seamless voice recording. 
With intuitive features and secure cloud storage, SoundJot offers a private and immersive journaling experience, 
enabling you to relive your memories anytime, anywhere.

Explore the comprehensive documentation for our application, SoundJot, and unlock a wealth of knowledge and guidance to enhance your audio journaling experience. [Click here](https://codelabs-preview.appspot.com/?file_id=1E2Z6QsyAEtmAuYTbtrClYIojHb8P_ISyPxjJWQZxXi8#0) to access a wealth of resources and start journaling with ease and creativity.

## Running the application
### Pre-requisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

### Steps to run application locally
1. Clone the repository
    ```bash
        git clone https://github.com/BigDataIA-Summer2023-Team2/Assignment3.git
    ```
2. Create a gcs_key.json file in airflow and streamlit folder with following variables defined
    ```json
    {
        "type": "service_account",
        "project_id": "xxx",
        "private_key_id": "xxx",
        "private_key": "xxx",
        "client_email": "clientname@projectid.iam.gserviceaccount.com",
        "client_id": "000",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/client_email",
        "universe_domain": "googleapis.com"
    }
    ```  
3. Create a kaggle.json file in airflow folder with following variables defined
    ```json
    {
        "username":"xxx",
        "key":"000"
    }
    ```
    
4. Create a .env file in the Project folder
    ```bash
    POSTGRES_USER="soundjot"
    POSTGRES_PASSWORD="soundjot"
    POSTGRES_DB="soundjot"
    POSTGRES_HOST="localhost"
    GOOGLE_APPLICATION_CREDENTIALS="/gcs_key.json"
    KAGGLE_DATASET_NAME="ejlok1/cremad,ejlok1/surrey-audiovisual-expressed-emotion-savee,uwrfkaggler/ravdess-emotional-speech-audio,ejlok1/toronto-emotional-speech-set-tess"
    AIRFLOW_UID=1000
    AIRFLOW_PROJ_DIR=./airflow
    KAGGLE_USERNAME = "xxx"
    KAGGLE_KEY = "xxx"
    DATA_DOWNLOAD_PATH="./data"
    LIBROSA_CACHE_DIR = '/tmp/librosa_cache'
    PINECONE_API_KEY="xxx"
    PINECONE_ENVIRONMENT="asia-southeast1-gcp-free"
    NUMBA_CACHE_DIR='/tmp'
    ```


5. Run the make command to build and deploy the application
    ```bash
        make build-up
    ```
6. Applciation would be accessible on localhost at following URLs \
    **Streamlit:** http://localhost:8090/ \
7. Destroying the deployed environment
    ```bash
        make down
    ```
## Project Tree
```
.
├── Makefile
├── README.md
├── airflow
│   ├── Dockerfile
│   ├── dags
│   │   ├── gcp_to_pinecone.py
│   │   ├── kaggle_to_gcp.py
│   │   ├── kaggle_to_pinecone.py
│   │   ├── populate_metadata.py
│   │   └── utils
│   ├── gcs_key.json
│   ├── kaggle.json
│   ├── kaggle.json:Zone.Identifier
│   └── requirements.txt
├── config
├── dags
├── docker-compose-local.yml
├── fastapi
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── utils
│       ├── db_utils
│       ├── gcp_utils
│       ├── generic
│       └── pinecone_utils
├── gcs_key.json
├── logs
├── plugins
├── streamlit
│   ├── Dockerfile
│   ├── Home.py
│   ├── gcs_key.json
│   ├── pages
│   │   ├── 1_User_Registration.py
│   │   ├── 2_User_Authentication.py
│   │   ├── 3_Upload_Audio.py
│   │   ├── 4_Show_Audio.py
│   │   ├── 5_Mood_Chart.py
│   │   └── __pycache__
│   ├── requirements.txt
│   ├── utils
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── backend.py
│   │   ├── db_utils
│   │   ├── gcp_utils
│   │   ├── generic
│   │   └── pinecone_utils
│   └── venv
│       ├── bin
│       ├── etc
│       ├── include
│       ├── lib
│       ├── lib64 -> lib
│       ├── pyvenv.cfg
│       └── share
└── tests
    └── pytest
        ├── default.py
        └── test.yaml
```

## References
- [SAVEE Kaggle](https://www.kaggle.com/ejlok1/surrey-audiovisual-expressed-emotion-savee)
- [RAVDESS Kaggle](https://www.kaggle.com/uwrfkaggler/ravdess-emotional-speech-audio)
- [TESS Kaggle](https://www.kaggle.com/ejlok1/toronto-emotional-speech-set-tess)
- [CREMA-D Kaggle](https://www.kaggle.com/ejlok1/cremad)
- [Baseline Model Kaggle](https://www.kaggle.com/code/ejlok1/audio-emotion-part-3-baseline-model/notebook)
- [Pinecone](https://docs.pinecone.io/docs/audio-search)
- [OpenAI](https://medium.com/muthoni-wanyoike/implementing-text-summarization-using-openais-gpt-3-api-dcd6be4f6933)

## Contributions

| Contributor    | Contibutions |
| -------- | ------- |
| Ashritha Goramane  |  |
| Rishabh Indoria    | 	|
| Parvati Sohani     |	|



