import streamlit as st
from openai import OpenAI

# Set page configuration
st.set_page_config(page_title="UI Page", layout="centered")
# Content in the sidebar
st.sidebar.image("/home/sharanya/AI_env/pinnacle_biologics/images/bee_chat.png",width=200)
st.sidebar.divider()

# Adding custom CSS to position the text at the bottom
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 15%;
        text-align: center;
        padding: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

# Adding the footer text at the bottom of the sidebar
st.sidebar.markdown("<div class='footer'>Powered by NeuronWorks.AI</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; font-size: 50px;'>🚀</div>", unsafe_allow_html=True)


# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize or retrieve the OpenAI model from session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# Initialize or retrieve chat history from session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def suggestion(question, response_placeholder):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Display user message in chat message container
    with response_placeholder.container():
        with st.chat_message("user"):
            st.markdown(question)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Create a stream of completions using OpenAI client
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
def app():
    # Accept user input
    prompt = st.chat_input("How can I help you?")

    if prompt:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
    
        st.session_state.messages.append({"role": "assistant", "content": response})


# Define options
options = [
    {"icon": "💡", "text": "Design a fun coding game"},
    {"icon": "✉️", "text": "Message to comfort a friend"},
    {"icon": "📚", "text": "Who is Raja Raja Cholan?"},
    {"icon": "✈️", "text": "Plan a relaxing day"},
]

# Display options side by side using st.columns
cols = st.columns(len(options))
response_placeholder = st.empty()  # Placeholder for the response
for col, option in zip(cols, options):
    with col:
        if st.button(f"{option['icon']} {option['text']}"):
            suggestion(option['text'], response_placeholder)

app()
