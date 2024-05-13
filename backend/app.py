from flask import Flask, request
import embeddings as EMBEDDINGS

app = Flask(__name__)
def run_generation(user_text, temperature, top_k, max_new_tokens, top_p):
    response = EMBEDDINGS.perform_rag_vector_search(user_text, temperature, top_k, max_new_tokens, top_p)
    #response = "user_text="+user_text+"temperature="+temperature+"top_k="+top_k+"max_new_tokens="+max_new_tokens+"top_p="+top_p
    return response

@app.route('/getresponse')
def getresponse():
    query = request.args.get("user_text")
    temperature = request.args.get("temperature")
    top_k = int(request.args.get("top_k"))
    max_new_tokens = request.args.get("max_new_tokens")
    top_p = request.args.get("top_p")
    response= run_generation(query,temperature,top_k,max_new_tokens,top_p)
    return response


if __name__ == "__main__":
    app.run(debug=True)


