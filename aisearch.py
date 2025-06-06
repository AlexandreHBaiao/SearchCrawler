# filepath: /home/azureuser/repos/SearchCrawler/aisearch.py
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    VectorSearchProfile,
    HnswAlgorithmConfiguration
)
from azure.identity import DefaultAzureCredential
from azure.identity import AzureCliCredential
from openai import AzureOpenAI
import uuid


service_name = "marcopsearch"
index_name = "vector-aisearch-wiki"

endpoint = f"https://{service_name}.search.windows.net"
credential = AzureCliCredential()  # Use Azure CLI credentials for authentication
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

token = credential.get_token("https://cognitiveservices.azure.com/.default").token
# Set the token for OpenAI
client = AzureOpenAI(azure_endpoint="https://ai-marcopinternhub651242772482.openai.azure.com/",
api_version="2023-03-15-preview",
api_key=token)

def create_index():
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content", type=SearchFieldDataType.String, retrievable=True, searchable=True),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            retrievable=False,
            vector_search_dimensions=1536,  # Set the dimensions of your vector embeddings
            vector_search_profile_name="vector-config",  # Reference the vector search configuration
        ),
    ]
    # all the documentation is incorret... poor copilot :-(
    vector_search = VectorSearch(
        profiles=[VectorSearchProfile(name="vector-config", algorithm_configuration_name="my-algorithms-config")],
        algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
    )
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    try:
        index_client.create_index(index)
    except Exception as e:
        print(f"Error creating index: {e}")
    finally:
        print(f"Index '{index_name}' created successfully.")
    

# Step 2: Generate embeddings using Azure OpenAI
def generate_embeddings(text):
    response = client.embeddings.create(input=text,
    model="text-embedding-ada-002")  # Replace with your deployed model name)
    return response.data[0].embedding


def upload_document(text):
    try:
        # Generate embeddings for the text
        embedding = generate_embeddings(text)

        # Create a document with the generated embedding
        document = {
            "id": str(uuid.uuid4()),  # generate a new unique ID for the document
            "content": text,
            "contentVector": embedding
        }

        # Upload the document to Azure Search
        search_client.upload_documents(documents=[document])
        print("Document uploaded successfully.")
    except Exception as e:
        print(f"Error uploading document: {e}")
    finally:
        print("Upload process completed.")
    # You can add more logic here to handle the response or errors

# example_text = "This is an example text to be indexed and searched."
# # # Uncomment the following line to create the index
# create_index()
# # # Uncomment the following line to upload a document
# upload_document(example_text)
# # # Uncomment the following line to search for a document     