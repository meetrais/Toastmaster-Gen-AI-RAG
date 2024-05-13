import gradio as gr
import requests
import warnings
warnings.filterwarnings("ignore")

def run_generation(user_text, temperature, top_k, max_new_tokens, top_p):
    
    #1 - Local 2- Docker 3- Azure
    ENVIRONMENT = 3
    PORT=str(5000)
    
    if ENVIRONMENT==1:
        BACKEND_SERVICE_ENDPOINT= "http://localhost:" + PORT
    elif ENVIRONMENT==2:
        BACKEND_SERVICE_ENDPOINT= "http://toastmaster-gen-ai-backend:" + PORT
    elif ENVIRONMENT==3:
        BACKEND_SERVICE_ENDPOINT= "https://tmbackendcontainerapp.nicesmoke-51dc90f5.southeastasia.azurecontainerapps.io"
    
    api = BACKEND_SERVICE_ENDPOINT
    api+= "/getresponse?user_text=" + user_text
    api+=  "&temperature=" + str(temperature) 
    api+=  "&top_k=" + str(top_k) 
    api+=  "&max_new_tokens=" + str(max_new_tokens)
    api+=  "&top_p=" + str(top_p)
    
    response = requests.get(api)
    return response.text

def main():
    # Gradio UI setup
    with gr.Blocks() as demo:
        with gr.Row():  
            with gr.Column(scale=4):
                user_text = gr.Textbox(placeholder="Write your question here", label="User input")
                model_output = gr.Textbox(label="Model output", lines=10, interactive=False)
                button_submit = gr.Button(value="Submit")

            with gr.Column(scale=1):
                max_new_tokens = gr.Slider(minimum=1, maximum=4000, value=250, step=1, label="Max New Tokens")
                top_p = gr.Slider(minimum=0.05, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)")
                top_k = gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Top-k")
                temperature = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, step=0.1, label="Temperature")

        user_text.submit(run_generation, [user_text, temperature, top_k, max_new_tokens, top_p], model_output)
        button_submit.click(run_generation, [user_text, temperature, top_k, max_new_tokens, top_p], model_output)

        #demo.queue(max_size=32).launch(server_port=7860)
        demo.launch()

if __name__ == "__main__":    
    #createmongodbdbandindex.create_mongodb_db_and_index()
    #EMBEDDINGS.CreateAndSaveEmbeddingsForPDFFile()
    main()