# Disciple AI

This is a simple AI chatbot that can answer questions about the Bible. 

## Demo
[![Watch the video](https://img.youtube.com/vi/nqfXXQzM2Yw/0.jpg)](https://www.youtube.com/watch?v=nqfXXQzM2Yw)


## Usage

create gcp postgres DB 

fill up env.exampe with information from DB

setup gcloud on your machine

run """ gcloud config set project {project_id} """ *replace the project_id with the project id of the DB*

run """ streamlit run dashboard.py """ to run locally 


## Roadmap

7/17/24 - added context window to ask follow up questions. (beta version)

### Credits to Moses Daudu for the notebook to get data, clean it, and organize the embeddings. 