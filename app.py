import os
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

PROMPT_TEMPLATE = """Answer the following question as best you can:

{input}

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: for SQL queries, write the query directly without any markdown formatting or code block syntax (no ```). Just write the pure SQL query.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important: When writing SQL queries:
- Do NOT use any backticks (```) or markdown formatting
- Write the SQL query directly
- Do NOT include 'sql' or any other language tags
- Keep the query clean and without any special formatting

Begin!

Question: {input}
Thought: Let me approach this step by step:
{agent_scratchpad}"""

class ChatWithSql:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def message(self, query):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=GOOGLE_API_KEY,
                temperature=0
                
            )
            
            db = SQLDatabase.from_uri(f"sqlite:///{self.db_name}")
            
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            tools = toolkit.get_tools()
            
            prompt = PromptTemplate(
                template=PROMPT_TEMPLATE,
                input_variables=["input", "agent_scratchpad", "tool_names", "tools"]
            )
            
            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt
            )
            
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True
            )
            
            response = agent_executor.invoke({"input": query})
            return response["output"]
            
        except Exception as e:
            return f"Error executing query: {str(e)}"

def clean_sql_query(query):
    query = query.replace('```sql', '').replace('```', '')
    return query.strip()

if __name__ == "__main__":
    try:
        obj = ChatWithSql("my_database.db")
        result = obj.message("What is the list of customer IDs and names?")
        print(result)
    except Exception as e:
        print(f"Main execution error: {str(e)}")