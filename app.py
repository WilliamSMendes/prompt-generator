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
# @st.cache_data(show_spinner=False, ttl=300)
# def call_mistral_api(prompt, temperature, system, max_length):
#     try:
#         output = replicate.run(
#         #"replicate-internal/mixtral-instruct-v0.1-fp16-triton-sm80:63888b8acf98421eb6ec992180ef3fbd2510f2ab18fcf368e76b13ccaf16d308",
#         "mistralai/mixtral-8x7b-instruct-v0.1",
#         input={
#                 "prompt": prompt,
#                 "temperature": temperature,
#                 "system_prompt": system,
#                 "max_new_tokens": max_length,
#                 "prompt_template": "<s>[INST] {prompt} [/INST]"
#             })
#         return output, None
    
#     except Exception as e:
#         return None, str(e)

# Function to reset the session state
def clear_cache():
    st.session_state['persona'] = ''
    st.session_state['tarefa'] = ''
    st.session_state['formato'] = ''
    st.cache_data.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# Sidebar
with st.sidebar:
    st.title('🧠 Modelo: meta-llama-3-70b-instruct')
    st.markdown("Características do modelo:")
    st.markdown(""" 
                - 70 bilhões de parâmetros
                - Limite de 128k de tokens de vocabulário
                - Supera o GPT-4 e Gemini 1.5 em diversas tarefas
                - Modelo de código aberto
                - Saber mais: [Meta AI](https://about.fb.com/br/news/2024/04/apresentando-meta-llama-3-o-grande-modelo-de-linguagem-de-codigo-aberto-mais-capaz-ate-hoje/)""")
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

persona = st.text_area('(Persona) Aja como...', value=st.session_state['persona'])
tarefa = st.text_area('(Tarefa) Crie um(a)...', value=st.session_state['tarefa'])
formato = st.text_area('(Formato) Me traga em forma de...', value=st.session_state['formato'])

st.session_state['persona'] = persona
st.session_state['tarefa'] = tarefa
st.session_state['formato'] = formato

button = st.button('Enviar')

if button:

    # prompt = f'''Você é um gerador de intruções para o chatGPT. Sua tarefa é criar um prompt personalizado com base nas informações fornecidas, e não realizar a tarefa em si. 
    # Por exemplo, se a persona for "Meu chefe", a tarefa for "enviar um email para o cliente sobre um atraso no projeto" e o formato for "deve retornar 3 opções de email para enviar ao cliente", sua tarefa seria criar um prompt assim:
    # "Imagine que você é meu chefe e precisa enviar um email a um cliente explicando um atraso no projeto devido a problemas técnicos imprevistos. Retorne o resultado em um formato que possa ser usado para criar 3 opções de emails para enviar ao cliente."
    # Agora, com base nesse exemplo, quero que você crie um prompt em português e detalhado com os seguintes detalhes: Aja como "{persona}", Crie um "{tarefa}", Me traga em forma de "{formato}". MAS SEM ASPAS'''

    prompt = f'''
    Você é um especialista em Criação de Prompt.
    Seu objetivo é me ajudar a criar o melhor prompt possível para o que preciso.

    O prompt que você fornecer deve ser escrito a partir da minha perspectiva (usuário), fazendo a solicitação ao ChatGPT.

    Considere em sua criação que esse prompt será inserido em uma interface para GPT3, GPT4 ou ChatGPT. Esse será o processo:

    Você irá gerar as seguintes seções:

    "
    Prompt:
    
    (Forneça o melhor prompt possível de acordo com minha solicitação)

    Sugestão de como melhorar seu prompt:
    
    (Forneça um parágrafo conciso sobre como melhorar o prompt. Seja muito crítico em sua resposta. Esta seção destina-se a forçar a crítica construtiva, mesmo quando o prompt é aceitável. Quaisquer suposições e/ou problemas devem ser incluídos)

    Aqui estão algumas perguntas que podem ajudar a enriquecer seu prompt:
    
    (faça quaisquer perguntas relacionadas a quais informações adicionais são necessárias de mim para melhorar o prompt (máximo de 3). Se o prompt precisar de mais esclarecimentos ou detalhes em determinadas áreas, faça perguntas para obter mais informações para incluir no prompt)
    "

    Com base nisso, minha solicitação é a seguinte:
    "ChatGPT, eu quero que você aja como um(a) {persona} e sua tarefa é criar um(a) {tarefa} e me traga a resposta em formato de {formato}"
    
    Responda em Português.
    '''

    # system = """
    # Seja criativo e detalhado, e gere um prompt que o usuário possa copiar e colar no chatGPT para ter uma resposta relevante e coerente.
    # NÃO EXECUTE A TAREFA, APENAS CRIE O PROMPT.
    # RESPONDA SEMPRE EM PORTUGUÊS
    # """

    system_prompt = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Seja criativo e detalhado, e gere um prompt que o usuário possa copiar e colar no chatGPT para ter uma resposta relevante e coerente.
    NÃO EXECUTE A TAREFA, APENAS CRIE O PROMPT.
    RESPONDA SEMPRE EM PORTUGUÊS<|eot_id|><|start_header_id|>user<|end_header_id|>
    {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """

    with st.spinner('Processando...'):
        try:
            output = client.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_length,
                    #"prompt_template": "<s>[INST] {prompt} [/INST]"
                    "prompt_template": system_prompt
                })
            
            output = "".join(output)
            
            st.subheader('🎉 Prompt gerado com sucesso 🎉')
            st.markdown(f'\n {output} \n')
        
        except Exception as e:
            st.error(f"Erro ao chamar a API: {e}")

    # if error:
    #     st.error(f"Erro ao chamar a API: {error}")

    # elif result:
    #     st.subheader('🎉 Prompt gerado com sucesso 🎉')
    #     st.markdown(f'\n {result} \n')

reseta = st.button('Resetar sessão')

if reseta:
    clear_cache()
    st.rerun()
