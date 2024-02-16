
import streamlit as st
import google.generativeai as genai

import os


os.environ["google_API_KEY"] = 'AIzaSyAGB5JvQRItM2CeZjLhJp-KKljxfuPBOzo'
genai.configure(api_key=os.getenv("google_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
def get_gemini_response(question, gender, age, weight, height, activity_level, goals, dietary_restrictions):
    text = f'Act as a fitness trainer and give a short but to the point answer according to the given information that I am {age} years old {gender}, my weight is {weight} kg, my height is {height}cm, i am {activity_level}, my goal is to {goals} and i am {dietary_restrictions}. my question is that {question}'
    response =chat.send_message(text,stream=True)
    return response

st.set_page_config(page_title="Fitness AI ChatBot", page_icon="🏋️‍♀️")

st.title("🔹🔷Fitee🔷🔹")
st.write("Made with ❤️ by Mainak")
with st.sidebar:
    gender = st.selectbox("Gender", ["male", "female"])
    age = st.number_input("Age", min_value=0, max_value=150, value=30)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=1.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=0.0,step=1.0, value=170.0)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    goals = st.radio("Goals", ["Loss Weight", "Maintain Weight", "Gain Weight"])
    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"])

if 'button_pressed' not in st.session_state:
        st.session_state.button_pressed = False

# Button to start conversation
start_conversation = st.button("Start Conversation")

if start_conversation or st.session_state.button_pressed:
    st.session_state.button_pressed = True
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    if prompt is None:
        response='Ask me anything about Fitness'
    else:
        with st.spinner('Typping...'):
            re = get_gemini_response(str(prompt), gender, age, weight, height, activity_level, goals, dietary_restrictions)
            response = ''
            for chunk in re:
                for ch in chunk.text.split(' '):
                    response += ch + ' '
            # res = []
            # for chunk in re:
            #     res.append(chunk.text)
            #     st.write(chunk.text)
                # print("_"*80)
            # re = re["output_text"]
            # re=return_response(str(prompt),document_search,chain)
    # response = re
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        if type(response)==str:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.markdown(response)      
            st.session_state.messages.append({"role": "assistant", "content": response})
