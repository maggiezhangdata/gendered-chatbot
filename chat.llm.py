import openai
from openai import OpenAI
import streamlit as st

# Set the title of the app
st.title("ChatGPT-like clone")

# Disclaimer expander
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "We appreciate your engagement! Please note, this demo is designed to process a maximum of 10 interactions. Thank you for your understanding."
    )

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize or retrieve the OpenAI model in the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize or retrieve the message history in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Maximum allowed messages
max_messages = 20  # 10 iterations of conversation (user + assistant)

# Check if the maximum message limit is reached
if len(st.session_state.messages) >= max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached. We value your interest!
        We encourage you to experience further interactions by building your own application with instructions
        from Streamlit's [Build conversational apps](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)
        tutorial. Thank you for your understanding."""
    )
else:
    # Input field for the user to type their message
    if prompt := st.chat_input("What is up?"):
        # Append the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare a placeholder for the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            # Call the OpenAI Chat Completions API
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            # Extract the full response
            full_response = response['choices'][0]['message']['content']
            message_placeholder.markdown(full_response)

            # Append the assistant's response to the session state
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
