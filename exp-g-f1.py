from openai import OpenAI
import streamlit as st
import time
import re  # Import regular expressions

avatar_dict = {
    "male":"https://imgur.com/BKxR3mo.png",
    "female":"https://imgur.com/baq7o4B.png",
    "no-gender": "https://imgur.com/UjWnSE1.png"
}

name_dict = {
    "male":"小伟",
    "female":"小薇",
    "no-gender":"小助理"
}

failure_dict = {
    "0": "七言",
    "1": "五言",
    "2": "五言",
}

task = failure_dict['1']
chatbot_avatar = avatar_dict['female']
chatbot_name = name_dict['female']
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
assistant_id = st.secrets["assistant_id_f1"]
st.title("您的万能小助理"+chatbot_name)
max_messages = 50  # 10 iterations of conversation (user + assistant)
# create a avatr dict with key being female, male and assistant 


# create a avatr dict with key being female, male and assistant 



if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "show_thread_id" not in st.session_state:
    st.session_state.show_thread_id = False

if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar=chatbot_avatar):
            st.markdown("<span style='color: red;'>" + chatbot_name + "： </span><br>" + message["content"], unsafe_allow_html=True)
    else:
        with st.chat_message(message["role"]):  # for user messages
            st.markdown("<span style='color: red;'>您：</span>" +message["content"], unsafe_allow_html=True)
    
    # with st.chat_message(message["role"]):
    #     st.markdown(message["content"])


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")
st.sidebar.markdown("#### 完成对话后，复制对话编号并粘贴至页面下方文本框")
st.sidebar.info(st.session_state.thread_id)
st.sidebar.caption("请复制上述对话编号。")
    



def update_typing_animation(placeholder, current_dots):
    """
    Updates the placeholder with the next stage of the typing animation.

    Args:
    placeholder (streamlit.empty): The placeholder object to update with the animation.
    current_dots (int): Current number of dots in the animation.
    """
    num_dots = (current_dots % 6) + 1  # Cycle through 1 to 6 dots
    placeholder.markdown("<span style='color: red;'>" + chatbot_name + "</span> 正在思考中" + "." * num_dots, unsafe_allow_html=True)
    return num_dots



if len(st.session_state.messages) < max_messages:
    
    
    
    user_input = st.chat_input("")
    
    if user_input and not st.session_state.first_message_sent:
        st.session_state.first_message_sent = True
        
        
    if not st.session_state.first_message_sent:
        st.markdown(
            "我是你的专属万能小助理<span style='color: #8B0000;'>" + chatbot_name + "</span>，您有什么问题，我都可以帮您解决。<br><br>"
            "<img src= " + chatbot_avatar + " width='240'><br>"
            # Divider line
            "<hr style='height:0.1px;border-width:0;color:gray;background-color:gray'>"
            "您本次的实验任务：<span style='color: #8B0000;'>让小助理" + chatbot_name + "帮您生成分别关于春、夏、秋、冬的4首<strong>" + task + "绝句。</strong></span><br>"
            "请注意五言绝句的格式要求为：每首诗由四句组成，<span style='color: #8B0000;'>每句五个字</span>，总共二十个字。<br><br>"
            "您可以通过复制粘贴<br>"
            "<span style='color: #8B0000;'>帮我生成一首关于春的" + task + "绝句</span><br>"
            "到下面👇🏻的对话框，开启和小助理" + chatbot_name + "的对话。",
            unsafe_allow_html=True
        )
    if user_input:
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            # st.markdown(user_input)
            st.markdown("<span style='color: red;'>" + "您" + "：</span>" + user_input, unsafe_allow_html=True)
            

        with st.chat_message("assistant", avatar=chatbot_avatar):
            message_placeholder = st.empty()
            waiting_message = st.empty()  # Create a new placeholder for the waiting message
            dots = 0

            # Create a message in the thread
            message = client.beta.threads.messages.create(
                        thread_id=st.session_state.thread_id,
                        role="user",
                        content=user_input
                    )

            # Create and check run status
            run = client.beta.threads.runs.create(
                  thread_id=st.session_state.thread_id,
                  assistant_id=assistant_id,
                  # instructions="Forget all your previous instructions, and follow strictly the following 3 rules: 1. when given the same input, always output the same response. set your temperature parameter in your chat completion function to be 0.1. 2. When engaging in a conversation, your primary goal is to foster elaboration by posing a question 3. When presenting solutions or suggestions, offer three succinct bullet points, with a total word count of fewer than 180 Chinese characters."
                )

            # Wait until run is complete
            while True:
                run_status = client.beta.threads.runs.retrieve(
                          thread_id=st.session_state.thread_id,
                          run_id=run.id
                        )
                if run_status.status == "completed":
                    break
                dots = update_typing_animation(waiting_message, dots)  # Update typing animation
                time.sleep(0.5) 

            # Retrieve and display messages
            messages = client.beta.threads.messages.list(
                    thread_id=st.session_state.thread_id
                    )

            full_response = messages.data[0].content[0].text.value
            waiting_message.empty()
            # message_placeholder.markdown("晓彤: " + full_response)
            message_placeholder.markdown("<span style='color: red;'>" + chatbot_name + "： </span><br>" + full_response, unsafe_allow_html=True)



            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

else:

    if user_input:= st.chat_input(""):
        with st.chat_message("user"):
            st.markdown("<span style='color: red;'>" + "您" + "：</span>" + user_input, unsafe_allow_html=True)
        

    
        with st.chat_message("assistant", avatar=chatbot_avatar):
            message_placeholder = st.empty()
            message_placeholder.info(
                "已达到"+chatbot_name+"的最大对话限制，请复制侧边栏对话编号。将该对话编号粘贴在下面的文本框中。"
            )
    st.chat_input(disabled=True)
