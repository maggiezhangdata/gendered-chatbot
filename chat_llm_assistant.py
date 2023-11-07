from openai import OpenAI
import streamlit as st

st.title("A ChatBot That Really Listens to You")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "We appreciate your engagement! Please note, this demo is designed to process a maximum of 10 interactions. Thank you for your understanding."
    )



client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# assistant_id = "asst_cejwvyELXSx6GzaD1hSe3g2L" # 10 words reply
assistant_id = st.secrets["assistant_id"]
thread = client.beta.threads.create()

if "messages" not in st.session_state:
    st.session_state.messages = []


# Displaying Previous Messages -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


max_messages = 20  # 10 iterations of conversation (user + assistant)

if len(st.session_state.messages) >= max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached..."""
    )
else:
    if user_input := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            message = client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=user_input
                    )

            run = client.beta.threads.runs.create(
                  thread_id=thread.id,
                  assistant_id=assistant_id,
                  instructions="Please address the user as test user. Your response should be exactly 10 words long."
                )
            # sleep for 6 secs


            run_status = client.beta.threads.runs.retrieve(
                          thread_id=thread.id,
                          run_id=run.id
                        )
            print(run_status.status)
        
            # wait until run is complete
            while run_status.status != "completed":
                run_status = client.beta.threads.runs.retrieve(
                          thread_id=thread.id,
                          run_id=run.id
                        )
                print(run_status.status)
                
                

            messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                    )

            print()
            print(messages.data)

            full_response = messages.data[0].content[0].text.value
            message_placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )






