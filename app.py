import streamlit as st

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

def main():
    chat_page()

if __name__ == '__main__':
    main()
