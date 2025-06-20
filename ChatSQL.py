import os
from dotenv import load_dotenv
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings

load_dotenv()

warnings.filterwarnings('ignore')

groq_api= os.getenv('GROQ_API_KEY')

model= ChatGroq(temperature=0, model= 'gemma2-9b-it',groq_api_key=groq_api)

db= SQLDatabase.from_uri(
    'mysql+pymysql://root:root@localhost/x',
    include_tables=['employees','departments','salaries']
)

write_query= create_sql_query_chain(model,db)

execute_query= QuerySQLDataBaseTool(db=db)

answer_query=PromptTemplate.from_template(""" 
Given the following user question, corresponding sql query, and sql result
generate a consise answer.

Question:{question}
Sql query: {query}
Sql result: {result}

Answer:
                                                                                                                                                                                                                                                           
""")

def extract_sql_query(llm_response):
    split_token='SQLQuery:'
    if split_token in llm_response:
        sql_part= llm_response.split(split_token,1)[1].strip()

        for stop_token in ['Question:','Answer:','\n\n']:
            if stop_token in sql_part:
                sql_part=sql_part.split(stop_token)[0].strip()

        return sql_part
    return llm_response

chain= (
    RunnablePassthrough.assign(
        query= lambda x: write_query.invoke({'question':x['question']}),
        result= lambda x: execute_query.invoke({'query': extract_sql_query(x['query'])}),
        answer= lambda x:answer_query.format(
            question= x['question'],
            query= x['query'],
            result= x['result']
        )
                )
                | {'response': model | StrOutputParser }

)

def query_database(question):
    llm_output= write_query.invoke({'question':question})

    sql_query= extract_sql_query(llm_output)

    sql_result= execute_query.invoke({'query': sql_query})

    final_answer= answer_query.format(
        question= question,
        query= sql_query,
        result= sql_result
    )

    response= model.invoke(final_answer)

    return response.content

result= query_database('minimum salary in the table?')
print(result)


