# Toastmaster-Gen-AI - WORK IN PROGRESS

## Introduction
Gen-AI specialized chatbot designed to answer fundamental questions about Toastmaster program. This project demonstrates how to develop retrieval augmented generation based chat-bot using Azure Open-AI service and Azure Cosmos-Db for Mongo-DB(VCore). Following are the main functionalities of this project.  
1. Create database, collection and vector-index in Mongo-DB(VCore) cluster.  
2. Create and save embeddings for PDF file in Mongo-DB(VCore) database.  
3. Perform plain vector search for user query/question.  
4. Perform chat-completion for user query/question.

## High Level Architecture Diagram
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/1999e549-42c7-4e22-b1a6-9e07c93c4b54)

## Code Walkthrough/Setup

### Azure Cosmos-DB for Mongo-DB(VCore) Cluster
Search for Azure Cosmos DB for MongoDB in the Azure portal and create cluster.  

![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/7f0a03a9-ee35-45f0-a310-5b3f3d565eba)

### Folder/File Structure
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/5966ffc6-dad2-49eb-8d5e-38b070a9bb21)

### Code overview
***backend***  
1. createmongodbdbandindex.py - Run this file to create database, collection and vector-index in Mongo-DB(VCore) cluster.  
2. embeddings.py - This file has below functions.  
   generate_embeddings - Generate embeddings for the text using Azure Open AI.  
   CreateAndSaveEmbeddingsForPDFFile - This function splits/chunks PDF file into pages, then creates embeddings and saves into MongoDB.  
   perform_vector_search - This function performs vector search on MongoDB vector-index for the user query. Then returns vector-search result.  
   perform_rag_vector_search - This function performs first vector-search and then RAG search by using OpenAI model defined for chat-completion.  
3. app.py - This file contains HTTP get method getresponse which is called in frontend app for vector-search based chat-completion.  
4. Dockerfile - This file is used to deploy backend app to docker.  
5. Create .env file in backend folder. Then add below environment variables and initialize with your values.  
6. requirements.txt - Contains list of Python libraries needed this program to run.  

AZURE_OPEN_AI_ENDPOINT=""  
AZURE_OPEN_AI_KEY=""  
AZURE_COSMOSDB_MONGODB_USERNAME=""  
AZURE_COSMOSDB_MONGODB_PASSWORD=""  
AZURE_COSMOSDB_MONGODB_CLUSTER=""  

***frontend***
1. app.py - To generate UI for Chat-Bot interface and call backend GET API for vector-search based chat-completion.
2. Dockerfile - This file is used to deploy frontend app to docker.
3. requirements.txt - Contains list of Python libraries needed this program to run.  

## Deployment

### Docker Deployment
Once you tested your backend and frontend apps in your local its time to deploy them to Docker. These commands are for Windows OS.  

Run below commands in the terminal of VS-Code/IDE to deploy and run backend app in Docker.  
cd backend  
docker build -t toastmaster-gen-ai-backend .  
docker run --name toastmaster-gen-ai-backend -p 5000:5000 -d toastmaster-gen-ai-backend  

Then run below commands to deploy and run frontend app in Docker.  
cd..  
cd frontend  
docker build -t toastmaster-gen-ai-frontend .  
docker run --name toastmaster-gen-ai-frontend -p 7860:7860 toastmaster-gen-ai-frontend  

Both the above containers needs to be in the same Docker network so run below commands.  
docker network create toastmaster-network
docker network connect toastmaster-network toastmaster-gen-ai-backend
docker network connect toastmaster-network toastmaster-gen-ai-frontend

### Azure Deployment
I use VS Code for development and deployments. So following steps use VS-Code and its Docker and Azure plugins. But you can also do all those steps using Azure CLI commands.

***Create Azure Container Registry***
1. In Docker plugin click on your Azure Subscription and select Create Registry then follow steps to create ACR. You may have to login to Azure.  
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/73f78e03-e779-4907-a234-e547ef942a98)

2. If you already have ACR in your Azure Subscription then you can connect to it as below.  
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/a3d4c095-9d25-4666-b72a-38e7c3abac79)

***Deploy Docker Image of Backend app to ACR***
1. In Docker plugin inside IMAGES section locate your Image of backend app and then right-click and select Tag option.
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/4fb0e850-a4e9-4288-857b-138be0ce1ee6)

2. Again right-click image and select Push option and follow steps to deploy your image to Azure Container Registry. 
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/ed837765-3e93-4b01-81fb-8dad02fdd01e)

***Create Azure Container App Environment***
1. In Azure plugin click on + sign to create new Azure resource, select "Create Container Apps Environment" option and then follow the steps. 
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/90cd3a8c-fb3c-4726-9130-835d6ff087b0)

2. Once your Container Apps Environment is created, right-click on it and select "Create Container App" and follow the steps. Select "Container Registry" option and use 5000 for port. While doing this select ACR and Image of backend app.
   ![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/9c38ed68-4c0f-4da6-bd6c-59b859319926)

   ![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/ac57d21d-5c6c-4066-8283-8a6046be71d9)

***Deploy Docker Image of frontend app to Azure Web-App***
1. Before we deploy docker image of frontend app to Azure Web-App, make below change in app.py so frontend app will call backend app endpoint deployed in Azure Container app. Then re-deploy image of frontend app to Docker.  
![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/573702b3-2546-4020-87f1-7111d0ea4d89)

2. In Docker plugin, IMAGES section righ-click on docker image of frontend app and push to ACR. Just like we tagged and pushed docker image of backend app above.

![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/d3fb3e63-c043-4f51-a551-84b609b2508b)

3. After that you should be able to see docker image of frontend app in your ACR like below. Now right click on that image and select option "Deploy Image to Azure App Service.". Follow the steps to create Azure App Service and Service Plan. It will also deploy your docker image of frontend app to Azure App Service.

![image](https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/46d0bc2d-0200-439c-8b2e-bec9baa81a19)

## Showtime
If you followed all the steps properly you should be able to see result of Retrieval Augmented Generation based Chat-Bot as below. 

<img width="827" alt="image" src="https://github.com/meetrais/Toastmaster-Gen-AI-RAG/assets/17907862/52a804c5-f648-487f-8a51-1b4d6af6a2dc">  

If it doesnt work then reach out to me and I will be happy to help.
