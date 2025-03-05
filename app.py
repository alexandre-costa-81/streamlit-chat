import streamlit as st

FILES_TYPES = [
    'Site',
    'Youtube',
    'PDF',
    'CSV',
    'TXT'
]

CONFIG_MODELS = {
    'Groq': {"models": ['llama-3.1-70b-versatile', 'gemma2-9b-it']},
    'OpenAI': {"models": ['gpt-4o-mini', 'gpt-4o','o1-preview', 'o1-mini']},
}

MESSAGE_EXAMPLE = [
    ('user', 'Olá'),
    ('assistant', 'Olá, como posso te ajudar?'),
    ('user', 'Quero saber o valor do dólar'),
    ('assistant', 'A cotação do dólar é R$ 5,50'),
]

def chat_page():
    st.header('Bem-vindo ao Oráculo', divider=True)

    messages = st.session_state.get('mensagens', MESSAGE_EXAMPLE)

    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])
    
    input_usuario = st.chat_input('Digite sua mensagem')

    if input_usuario:
        messages.append(('user', input_usuario))
        st.session_state['mensagens'] = messages
        st.rerun()

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

def main():
    chat_page()
    with st.sidebar:
        sidebar()

if __name__ == '__main__':
    main()
