from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
import environ


env = environ.Env()
environ.Env.read_env()

API_KEY = env('OPENAI_API_KEY')

# Setup database
db_uri = f"postgresql+psycopg://postgres:{env('DBPASS')}@localhost:5432/{env('DATABASE')}"
db = SQLDatabase.from_uri(db_uri)

# setup llm
llm = ChatOpenAI(temperature=0, openai_api_key=API_KEY)

# Create db chain
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

pyQuestion: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

# Setup the database chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=API_KEY) 
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                print(db_chain.invoke(question))
            except Exception as e:
                print(e)

get_prompt()
