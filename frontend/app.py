import gradio as gr
import warnings
warnings.filterwarnings("ignore")

def run_generation(user_text, temperature, top_k, max_new_tokens, top_p):
    response = "Something"
    return response

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