import os
import replicate
import streamlit as st
#from dotenv import load_dotenv

# Load API key
# load_dotenv()
# api_key = os.getenv("MISTRAL_API_KEY")
# if not api_key:
#     st.error("Erro: Chave da API não encontrada.")
#     st.stop()

if 'MISTRAL_API_KEY' in st.secrets:
    api_key = st.secrets['MISTRAL_API_KEY']
else:
    st.error("Erro: Chave da API não encontrada.")
    st.stop()

os.environ['MISTRAL_API_KEY'] = api_key

client = replicate.Client(api_token=api_key)

# App title
st.set_page_config(page_title="💬 Gerador de Prompts")

# Function to call the API
@st.cache_data(show_spinner=False, ttl=300)
def call_mistral_api(prompt, temperature, system, max_length):
    try:
        output = ""
        for event in client.stream(
            "mistralai/mixtral-8x7b-instruct-v0.1",
            input={
                "prompt": prompt,
                "temperature": temperature,
                "system_prompt": system,
                "max_new_tokens": max_length,
                "prompt_template": "<s>[INST] {prompt} [/INST]"
            },
        ):
            output += str(event)
        return output, None
    except Exception as e:
        return None, str(e)

# Function to reset the session state
def clear_cache():
    st.session_state['persona'] = ''
    st.session_state['tarefa'] = ''
    st.session_state['formato'] = ''
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# Sidebar
with st.sidebar:
    st.title('🧠 Modelo: mixtral-8x7b-instruct-v0.1')
    st.markdown("Características do modelo:")
    st.markdown(""" 
                - 47 bilhões de parâmetros
                - Limite de 32k de tokens de vocabulário
                - Supera o GPT-3.5 e Llama 2 em diversas tarefas
                - Resposta 6x mais rapida do que os concorrentes
                - Modelo de código aberto
                - Saber mais: [MistralAI](https://mistral.ai/news/mixtral-of-experts/)""")
    st.markdown(" ")
    st.subheader('🛠️ Parâmetros do modelo')
    st.markdown(" ")
    temperature = st.sidebar.slider('Temperatura', 
                                    min_value=0.0, 
                                    max_value=1.0, 
                                    value=0.7, 
                                    step=0.1)
    st.markdown('A temperatura controla o quanto o modelo pode ser criativo')
    st.markdown(" ")
    max_length = st.sidebar.slider('Comprimento Máximo', 
                                   min_value=32, 
                                   max_value=4096, 
                                   #value=120,
                                   value=1024, 
                                   step=8)
    st.markdown('O comprimento máximo define o tamanho das respostas geradas pelo modelo')
    st.markdown(" ")
    st.markdown("------------------------------")
    st.markdown(" ")
    
    st.subheader('✨ Criacionistas ✨')
    st.markdown('🔬 [Will](https://www.linkedin.com/in/williamsm01010101/)')
    st.markdown('🎨 [Tabs](https://www.linkedin.com/in/t%C3%A1bata-martins-9a5383131/)')

# Inputs
st.title('💬 Gerador de Prompts')
st.markdown('📝 Preencha os campos para gerar um prompt personalizado')

# Using session state to maintain input state
if 'persona' not in st.session_state:
    st.session_state['persona'] = ''
if 'tarefa' not in st.session_state:
    st.session_state['tarefa'] = ''
if 'formato' not in st.session_state:
    st.session_state['formato'] = ''

persona = st.text_area('Aja como...', value=st.session_state['persona'])
tarefa = st.text_area('Crie um...', value=st.session_state['tarefa'])
formato = st.text_area('Me traga em forma de...', value=st.session_state['formato'])

st.session_state['persona'] = persona
st.session_state['tarefa'] = tarefa
st.session_state['formato'] = formato

button = st.button('Enviar')

if button:

    prompt = f'''Você é um gerador de intruções para o chatGPT. Sua tarefa é criar um prompt personalizado com base nas informações fornecidas, e não realizar a tarefa em si. Por exemplo, se a persona for "Meu chefe", a tarefa for "enviar um email para o cliente sobre um atraso no projeto" e o formato for "deve retornar 3 opções de email para enviar ao cliente", sua tarefa seria criar um prompt assim:
    "Imagine que você é meu chefe e precisa enviar um email a um cliente explicando um atraso no projeto devido a problemas técnicos imprevistos. Retorne o resultado em um formato que possa ser usado para criar 3 opções de emails para enviar ao cliente."
    Agora, com base nesse exemplo, quero que você crie um prompt em português e detalhado com os seguintes detalhes: Aja como "{persona}", Crie um "{tarefa}", Me traga em forma de "{formato}". MAS SEM ASPAS'''

    system_prompt = """
    Seja criativo e detalhado, e gere um prompt que o usuário possa copiar e colar no chatGPT para ter uma resposta relevante e coerente.
    NÃO EXECUTE A TAREFA, APENAS CRIE O PROMPT.
    RESPONDA SEMPRE EM PORTUGUÊS.
    """

    with st.spinner('Processando...'):
        result, error = call_mistral_api(prompt, temperature, system_prompt, max_length)

    if error:
        st.error(f"Erro ao chamar a API: {error}")

    elif result:
        st.subheader('🎉 Prompt gerado com sucesso 🎉')
        st.markdown(f'\n {result} \n')

reseta = st.button('Resetar sessão')

if reseta:
    clear_cache()
    st.rerun()