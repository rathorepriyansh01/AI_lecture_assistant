from backend.services.retrieval_service import RetrieverService

print("1. Import Successful")

retriever = RetrieverService()

print("2. Retriever Initialized")

question = input("Question: ")

print("3. Question Received")

response = retriever.retrieve(question)

print("4. Retrieve Finished")

print(response)