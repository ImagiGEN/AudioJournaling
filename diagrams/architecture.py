# diagram.py
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.gcp.database import Datastore
from diagrams.onprem.client import Users
from diagrams.gcp.database import SQL
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import Postgresql
from diagrams.programming.framework import Fastapi
from diagrams.custom import Custom



with Diagram("Architecture", show=False):
    
    #streamlit = Custom("", "./myresources/streamlit.png")
    #pinecone = Custom("Store Embeddings", "./myresources/pinecone.jpeg")
    # huggingface = Custom("Huggingface Model", "./myresources/huggingface.png")
    # openai = Custom("LLM","./myresources/openai.png")
    # kaggle = Custom("Dataset","./myresources/kaggle.png")
   # tensorflow = Custom("Model Training Pipeline", "./myresources/tensorflow.png")
    # datastore = Custom("Datastore","./myresources/gcs.png")
    #modelstore = Custom("Model store","./myresources/gcp.png")
    user  = Users("Users") 
    #database = SQL("Database")
    #dag = Airflow("Store data DAG")
    # postgresql = Postgresql("RDBMS")
    #embeddings = Custom("Generate Embeddings","./myresources/embeddings.png")
    # prediction = Custom("Audio Emotion Prediction","./myresources/prediction.png")
    # fastapi = Custom("FastAPI","./myresources/fastapi.png")
    #python = Custom("Explore Data","./myresources/python.png")

   # with Cluster("Model"):

    #    model = [Custom("Dataset","./myresources/kaggle.png") >> Custom("Explore Data","./myresources/python.png") >> Custom("Model Training Pipeline", "./myresources/tensorflow.png") >>  Custom("Model store","./myresources/gcp.png")]
          
    with Cluster("Embeddings") as embeddings:

        panns_inf = Custom("Generate Embeddings","./myresources/ml_model.png")
        pinecone = Custom("Store Embeddings", "./myresources/pinecone.png")
        panns_inf >> Edge(label="Embeddings-Index") << pinecone
    
    with Cluster("Storage") as storage:
        dbms = Postgresql("RDBMS")
        model_store = Custom("Model store","./myresources/gcs.png")
        datastore = Custom("Datastore","./myresources/gcs.png")

    with Cluster("Front End") as frontend:
        streamlit = Custom("UI", "./myresources/streamlit.png")
    
    with Cluster("Back End") as backend:
        fastapi = Custom("FastAPI","./myresources/fastapi.png")
        prediction = [Custom("Audio Emotion Prediction","./myresources/prediction.png")]
        #data >> backend
    
    with Cluster("Model") as model:
        openai = Custom("LLM","./myresources/openai.png")
        huggingface = Custom("Huggingface Model", "./myresources/huggingface.png")


    user >> Edge(label="(1) Jot Journal\nAudio Library\nChapters\nMood Chart (10)") << streamlit
    streamlit >> Edge(label="(2) Audio\nMetadata\n\n (9)Quote\nSummary") << fastapi
    fastapi >> Edge(label="(3) Audio file") - datastore
    fastapi >> Edge(label="(4) Audio Metadata") << dbms
    fastapi >> Edge(label="(5) Audio\n\n(6) Emotion") << panns_inf 
    fastapi >> Edge(label="(7) Transcript\nEmotion\n\n (8) Quote\nSummary") << openai
