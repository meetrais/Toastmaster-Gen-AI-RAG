import embeddings as EMBEDDINGS
import createmongodbdbandindex

if __name__ == "__main__":
    #InitializeEmbeddingsForPDFFile()
    #print(embeddings)
    results = EMBEDDINGS.perform_vector_search("Do you have anything very sweet?")
    for result in results:
        EMBEDDINGS.print_product_search_result(result)
     #EMBEDDINGS.CreateAndSaveEmbeddingsForPDFFile()
     #createmongodbdbandindex.create_mongodb_db_and_index()