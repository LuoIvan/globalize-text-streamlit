import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you. 
    - Professional : Thank you for the opportunity to interview on-site at the Marshall & Ilsley office in Milwaukee. I found my observation hour in the Loan Department very interesting and was impressed with the total number of customers and accounts that are being reviewed on a daily basis.
    - Polite : If you can finish the edit by this afternoon, we can get it to the client by EOD.
    - Pessimistic : I got diagnosed with cancer and my dog died. I just don't believe that anything will get better anytime soon.
    - Optimistic : Despite the civil unrest happening in my city, I believe I can make things better and see real change in my lifetime.
    - Tense : She frantically searched the room for the killer, who she knew was hidden somewhere in the darkness. Moving blindly through the space, she wondered whether she would find him and stop him before it was too late and he moved on to his next victim.
    - Curious : He continued to ask questions as we drove to school, wondering about the color of the sky, why the birds were flying in a V-shaped pattern and whether I would be there to pick him up after his nap.
    - Uplifting : Jason knew that the first day being back at school in his new wheelchair would be difficult, but he remembered his mother's advice to go through the day with a smile on his face. He wheeled himself into school, only to find that his friends and fellow students were happy to give his chair a push and sit with him, offering friendly and encouraging words.
    - Aggressive : The answer is no, and I don't want to hear another word about it for as long as we both live.
    - Assertive : As she spoke, her conviction was unshakeable and those listening felt moved to join the committee and make changes in their community.
    - Informative : The human brain contains millions of cells, all working to handle the various functions performed by the human body.
    - Entertaining : Knock-knock, who's there? Nobel. Nobel who? No bell, that's why I knocked on the door.
    - Sarcastic : Rolling her eyes, Emma responded to the bully, ‘Okay, whatever you say goes,' and then forcefully walked away.
    - Cooperative : After I present my plan for the new project, I would love to hear your thoughts and will open the meeting up to sharing by everyone on the team.

    Here are some phases need be removed in different Tones:
    - Confident : I think, I’d like to, I’m hoping to
    
    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

email_content = ""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)

st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal', 'Professional', 'Polite', 'Confident', 'Pessimistic', 'Optimistic', 'Tense', 'Curious', 'Uplifting', 'Aggressive', 'Assertive', 'Informative', 'Entertaining', 'Sarcastic', 'Cooperative'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
