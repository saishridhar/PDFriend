from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub


def get_conversation_chain(vdb):
    memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = HuggingFaceHub(repo_id='google/flan-t5-xxl',model_kwargs={'temperature':0.5,'max_length':2048}),
        retriever=vdb.as_retriever(),
        memory=memory
    )
    return conversation_chain
