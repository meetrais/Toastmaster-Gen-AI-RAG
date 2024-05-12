# Toastmaster-Gen-AI - WORK IN PROGRESS

## Introduction
Gen-AI specialized chatbot designed to answer fundamental questions about Toastmaster program. This project demonstrates how to develop retrieval sugmented generation based chat-bot using Azure Open-AI service and Azure Cosmos-Db for Mongo-DB VCore. Following are main functionalities of this project.  
1. Create database, collection and vector-index in Mongo-DB VCore cluster.  
2. Create and save embeddings for PDF file in Mongo-DB VCore database.  
3. Perform plain vector search for user query/question.  
4. Perform chat-completion for user query/question.
   
## Code Overview
### Folder/File Structure
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/5966ffc6-dad2-49eb-8d5e-38b070a9bb21)

cd backend
docker build -t toastmaster-gen-ai-backend .
docker run --name toastmaster-gen-ai-backend -p 5000:5000 -d toastmaster-gen-ai-backend

cd..
cd frontend
docker build -t toastmaster-gen-ai-frontend .
docker run --name toastmaster-gen-ai-frontend -p 7860:7860 toastmaster-gen-ai-frontend

docker network create toastmaster-network
docker network connect toastmaster-network toastmaster-gen-ai-backend
docker network connect toastmaster-network toastmaster-gen-ai-frontend

https://code.visualstudio.com/docs/containers/app-service