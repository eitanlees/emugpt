import sys

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

SQL_DB_NAME = "chat.db"

session_name = input("Enter Session Name: ")
config = {"configurable": {"session_id": session_name}}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI() | StrOutputParser()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string=f"sqlite:///{SQL_DB_NAME}"
    ),
    input_messages_key="question",
    history_messages_key="history",
)

while True:
    q = input(">>> ")
    if (q == "q") or (q == "exit"):
        sys.exit()

    for chunk in chain_with_history.stream({"question": q}, config=config):
        print(chunk, end="", flush=True)
    print()
