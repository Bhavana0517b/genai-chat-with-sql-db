import streamlit as st
from pathlib import Path
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from langchain_groq import ChatGroq

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# from langchain.agents.agent_types import AgentType

st.set_page_config(page_title="langchain:Chat with SQL DB")
st.title("Langchain:Chat with SQL DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite 3 Database- Student.db", "connect to you SQL Database"]
selected_opt=st.sidebar.radio(label="choose the DB which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MY SQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL Password", type="password")
    mysql_db=st.sidebar.text_input("MYSQL database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="Groq API Key", type="password")

if not db_uri:
    st.info("please enter the database information and uri")

if not api_key:
    st.info("please add the groq api key")
    st.stop()

##LLM model
llm=ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-20b", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None,
                 mysql_password=None, mysql_db=None):

    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(
            f"file:{dbfilepath}?mode=ro",
            uri=True
        )
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()

        connection_url = URL.create(
            drivername="mysql+mysqlconnector",
            username=mysql_user,
            password=mysql_password,
            host=mysql_host,
            database=mysql_db,
        )

        engine = create_engine(connection_url)

        return SQLDatabase(engine)

# @st.cache_resource(ttl="2h")
# def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
#     if db_uri==LOCALDB:
#         dbfilepath=(Path(__file__).parent/"student.db").absolute()
#         print(dbfilepath)
#         creator=lambda:sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator))
#     elif db_uri==MYSQL:
#         if not (mysql_host and mysql_user and mysql_password and mysql_db):
#             st.error("please provide al MYSQL connection details.")
#             st.stop()
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

if db_uri==MYSQL:
    db=configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db=configure_db(db_uri)

##toolkit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="tool-calling"
)

if "messages" not in st.session_state or st.sidebar.button("clear message history"):
    st.session_state["messages"]=[{"role":"assistant", "content":"How can i help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="ask anything from the database")

if user_query:
    st.session_state.messages.append({"role":"user", "content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant", "content":response})
        st.write(response)