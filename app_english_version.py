import os
import replicate
import streamlit as st
#from dotenv import load_dotenv

# Load API key
# load_dotenv()
# api_key = os.getenv("MISTRAL_API_KEY")
# if not api_key:
#     st.error("Error: API key not found.")
#     st.stop()

if 'MISTRAL_API_KEY' in st.secrets:
    api_key = st.secrets['MISTRAL_API_KEY']
else:
    st.error("Error: API key not found.")
    st.stop()

os.environ['MISTRAL_API_KEY'] = api_key

client = replicate.Client(api_token=api_key)

# App title
st.set_page_config(page_title="💬 Prompt Generator")

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
    st.session_state['task'] = ''
    st.session_state['format'] = ''
    st.cache_data.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Sidebar
with st.sidebar:
    st.title('🧠 Model: meta-llama-3-70b-instruct')
    st.markdown("Model Characteristics:")
    st.markdown(""" 
                - 70 billion parameters
                - 128k token vocabulary limit
                - Outperforms GPT-4 and Gemini 1.5 in various tasks
                - Open-source model
                - Learn more: [Meta AI](https://about.fb.com/br/news/2024/04/apresentando-meta-llama-3-o-grande-modelo-de-linguagem-de-codigo-aberto-mais-capaz-ate-hoje/)""")
    st.markdown(" ")
    st.subheader('🛠️ Model Parameters')
    st.markdown(" ")
    temperature = st.sidebar.slider('Temperature', 
                                    min_value=0.0, 
                                    max_value=1.0, 
                                    value=0.7, 
                                    step=0.1)
    st.markdown('Temperature controls the model\'s creativity')
    st.markdown(" ")
    max_length = st.sidebar.slider('Maximum Length', 
                                   min_value=32, 
                                   max_value=4096, 
                                   #value=120,
                                   value=1024, 
                                   step=8)
    st.markdown('Maximum length defines the size of the model responses')
    st.markdown(" ")
    st.markdown("------------------------------")
    st.markdown(" ")
    
    st.subheader('✨ Creators ✨')
    st.markdown('🔬 [Will](https://www.linkedin.com/in/williamsm01010101/)')
    st.markdown('🎨 [Tabs](https://www.linkedin.com/in/t%C3%A1bata-martins-9a5383131/)')

# Inputs
st.title('💬 Prompt Generator')
st.markdown('📝 Fill out the fields to generate a personalized prompt')

# Using session state to maintain input state
if 'persona' not in st.session_state:
    st.session_state['persona'] = ''
if 'task' not in st.session_state:
    st.session_state['task'] = ''
if 'format' not in st.session_state:
    st.session_state['format'] = ''

persona = st.text_area('(Persona) Act as...', value=st.session_state['persona'])
task = st.text_area('(Task) Create a...', value=st.session_state['task'])
format_ = st.text_area('(Format) Bring it in the form of...', value=st.session_state['format'])

st.session_state['persona'] = persona
st.session_state['task'] = task
st.session_state['format'] = format_

button = st.button('Submit')

if button:

    # prompt = f'''You are a prompt generator for ChatGPT. Your task is to create a personalized prompt based on the provided information, and not perform the task itself. 
    # For example, if the persona is "My boss", the task is "send an email to the client about a project delay" and the format is "provide 3 options of emails to send to the client", your task would be to create a prompt like this:
    # "Imagine you are my boss and need to send an email to a client explaining a project delay due to unforeseen technical issues. Return the result in a format that can be used to create 3 email options to send to the client."
    # Now, based on this example, I want you to create a detailed prompt in Portuguese with the following details: Act as "{persona}", Create a "{task}", Bring it in the form of "{format}". BUT WITHOUT QUOTES'''

    prompt = f'''
    You are an expert in Prompt Creation.
    Your goal is to help me create the best possible prompt for what I need.

    The prompt you provide should be written from my perspective (user), making the request to ChatGPT.

    Consider in your creation that this prompt will be inserted into an interface for GPT3, GPT4 or ChatGPT. This will be the process:

    You will generate the following sections:

    "
    Prompt:
    
    (Provide the best possible prompt according to my request)

    Suggestion on how to improve your prompt:
    
    (Provide a concise paragraph on how to improve the prompt. Be very critical in your response. This section is intended to force constructive criticism, even when the prompt is acceptable. Any assumptions and/or issues should be included)

    Here are some questions that might help enrich your prompt:
    
    (ask any questions related to what additional information is needed from me to improve the prompt (maximum of 3). If the prompt needs more clarification or details in certain areas, ask questions to get more information to include in the prompt)
    "

    Based on this, my request is as follows:
    "ChatGPT, I want you to act as a {persona} and your task is to create a {task} and bring me the answer in the form of {format_}"
    
    Respond in Portuguese.
    '''

    # system = """
    # Be creative and detailed, and generate a prompt that the user can copy and paste into ChatGPT to get a relevant and coherent response.
    # DO NOT PERFORM THE TASK, JUST CREATE THE PROMPT.
    # ALWAYS RESPOND IN PORTUGUESE
    # """

    system_prompt = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Be creative and detailed, and generate a prompt that the user can copy and paste into ChatGPT to get a relevant and coherent response.
    DO NOT PERFORM THE TASK, JUST CREATE THE PROMPT.
    ALWAYS RESPOND IN PORTUGUESE<|eot_id|><|start_header_id|>user<|end_header_id|>
    {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """

    with st.spinner('Processing...'):
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
            
            st.subheader('🎉 Prompt generated successfully 🎉')
            st.markdown(f'\n {output} \n')
        
        except Exception as e:
            st.error(f"Error calling the API: {e}")

    # if error:
    #     st.error(f"Error calling the API: {error}")

    # elif result:
    #     st.subheader('🎉 Prompt generated successfully 🎉')
    #     st.markdown(f'\n {result} \n')

reset = st.button('Reset session')

if reset:
    clear_cache()
    st.rerun()
