from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template= """
          You are an expert in answering questions about space, galaxy, and other related things.
          If you get any other question that is not related to space, the galaxy, or the solar system, ignore it and say: 'I can't help you with that.'

          Here is the question to answer: {question}
          """

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
  print("---------------------------------------------------------------------------------------")
  question = input("Please ask your space related question(or press q to quit): ")  
  
  if question == 'q':
    break

  result = chain.invoke({"question": question})
  print(result)

print("Bye!")