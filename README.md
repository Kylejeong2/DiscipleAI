# Disciple AI

This is a simple AI chatbot that can answer questions about the Bible. 

## Usage

create gcp postgres DB 

fill up env.example with information from DB

setup gcloud on your machine

run """ gcloud config set project {project_id} """ *replace the project_id with the project id of the DB*

run """ streamlit run dashboard.py """ to run locally 


## Roadmap

7/17/24 - added context window to ask follow up questions.

### Credits to Moses Daudu for the notebook to get data, clean it, and organize the embeddings. 