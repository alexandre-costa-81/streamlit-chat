
import streamlit as st
import tempfile
import certifi

from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from loaders import load_website, load_youtube, load_csv, load_pdf, load_text

FILES_TYPES = [
    'Site',
    'Youtube',
    'PDF',
    'CSV',
    'TXT'
]

CONFIG_MODELS = {
    'Groq': {"models": ['llama-3.3-70b-specdec', 'deepseek-r1-distill-qwen-32b', 'qwen-2.5-32b'], 'chat': ChatGroq},
    'OpenAI': {"models": ['gpt-4o-mini', 'gpt-4o','o1-preview', 'o1-mini'], 'chat': ChatOpenAI},
}

def load_files(file_type, value):
    if file_type == 'Site':
        returned = load_website(value)
    elif file_type == 'Youtube':
        returned = load_youtube(value)
    elif file_type == 'PDF':
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
            temp.write(value.read())
            temp_name = temp.name
        returned = load_pdf(temp_name)
    elif file_type == 'CSV':
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp:
            temp.write(value.read())
            temp_name = temp.name
        returned = load_csv(temp_name)
    elif file_type == 'TXT':
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp:
            temp.write(value.read())
            temp_name = temp.name
        returned = load_text(temp_name)
    
    return returned

def load_model(provider, model, api_key, file_type, value):
    document = load_files(file_type, value)

    chat = CONFIG_MODELS[provider]['chat'](model=model, api_key=api_key)
    st.session_state['chat'] = chat

def chat_page():
    st.header('Bem-vindo ao Oráculo', divider=True)

    chat_model = st.session_state.get('chat')
    messages = st.session_state.get('mensagens', ConversationBufferMemory())

    for message in messages.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)
    
    user_input = st.chat_input('Digite sua mensagem')

    if user_input:
        messages.chat_memory.add_user_message(user_input)
        chat = st.chat_message('human')
        chat.markdown(user_input)

        chat = st.chat_message('ai')
        response = chat.write_stream(chat_model.stream(user_input))

        messages.chat_memory.add_ai_message(response)

        st.session_state['mensagens'] = messages

def sidebar():
    tabs = st.tabs(['Upload de arquivos', 'Seleção de Modelos'])
    with tabs[0]:
        file_type = st.selectbox('Selecione o tipo de arquivo', FILES_TYPES)
        if file_type == 'Site':
            returned = st.text_input('Digite a URL do site')
        elif file_type == 'Youtube':
            returned = st.text_input('Digite a URL do vídeo')
        elif file_type == 'PDF':
            returned = st.file_uploader('Faça o upload do arquivo', type='pdf')
        elif file_type == 'CSV':
            returned = st.file_uploader('Faça o upload do arquivo', type='csv')
        elif file_type == 'TXT':
            returned = st.file_uploader('Faça o upload do arquivo', type='txt')
    with tabs[1]:
        provider = st.selectbox('Selecione o provedor de modelos', CONFIG_MODELS.keys())
        model = st.selectbox('Selecione o modelo', CONFIG_MODELS[provider]['models'])
        api_key = st.text_input(
            f'Digite a chave da API para o provedor {provider}',
            value=st.session_state.get(f'api_key_{provider}')
        )
        st.session_state[f'api_key_{provider}'] = api_key

        if st.button('Carregar modelo', use_container_width=True):
            load_model(provider, model, api_key, file_type, returned)

def main():
    chat_page()
    with st.sidebar:
        sidebar()

if __name__ == '__main__':
    main()
