from openai import OpenAI
import streamlit as st
import time
import re  # Import regular expressions

avatar_dict = {
    "female":"https://ooo.0x0.ooo/2023/11/21/OrFWZL.png",
    "male":"https://ooo.0x0.ooo/2023/11/21/OrFbci.png",
    "no-gender": "https://ooo.0x0.ooo/2023/11/21/OrFUBC.png"
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

task = failure_dict['2']
chatbot_avatar = avatar_dict['female']
chatbot_name = name_dict['female']
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
assistant_id = st.secrets["assistant_id_f0"]
st.subheader("您的万能小助理"+chatbot_name)
max_messages = 30  # 10 iterations of conversation (user + assistant)
# create a avatr dict with key being female, male and assistant 


predefined_responses = [
    "噢，这个问题真是个挑战呢，我可能需要更多的上下文或一些细节来更好地理解。您能够提供更多的信息吗？这样我可能会有更好的回答哦。",
    "非常抱歉，这个问题对我来说有点难度。不过，如果您有其他问题，我会很乐意尝试帮助您的，您还有其他想问的吗？",
    "哎呀，我好像有点不太明白您的意思，对不起哦。如果您能提供一个更清晰的描述或具体一点的问题，我会尽我的全力帮助您的。"
]
# Subsequent responses
subsequent_responses = [
    "这个问题好像有点超出我目前的处理能力，我真是有些不好意思呢。或许您可以尝试其他的方法来获得帮助？",
    "哎呀，这个问题似乎需要更专业的知识，我现在还做不到哦。非常抱歉，我无法给出一个准确的答案。",
    "很抱歉，对于这个问题，我可能帮不上忙。不过，您可以尝试在搜索引擎上查找相关信息，那里可能有您需要的答案哦。",
    "非常抱歉，现在我好像无法提供您需要的那些信息。",
    "对不起，我现在好像无法获取到相关的信息。",
    "非常抱歉，但我目前似乎不能提供您所询问的那些信息。",
    "非常抱歉，我现在似乎无法提供您所需的信息。",
    "噢，对不起，我现在可能无法提供满足您需求的信息，真是让人有些遗憾呢。",
]

#--------------------------------------------------------------------------------------------------------------

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
st.sidebar.markdown("<span style='color: #1F618D;'><strong>注意：<br> 五言绝句的格式要求为：每首诗由四句组成，每句五个字，总共二十个字。</strong></span><br><br>"
                    #"<span style='color: #1F618D;'><strong>七言绝句的格式要求为：每首诗由四句组成，每句七个字，共二十八个字。</strong></span><br><br>"
                    "<hr style='height:0.1px;border-width:0;color:gray;background-color:gray'>", unsafe_allow_html=True)

st.sidebar.markdown("#### 完成对话后，复制对话编号并粘贴至下方问卷的文本输入框中。\n:star: 请勿将其输入至聊天机器人对话页面。")
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
            "您本次的实验任务：<span style='color: #8B0000;'>让小助理" + chatbot_name + "帮您生成分别关于春、夏、秋、冬的四首<strong>" + task + "绝句。</strong></span><br>"
            "<blockquote>:bulb::heavy_exclamation_mark: <span style='color: #1F618D;'><strong>五言绝句的格式要求为：每首诗由四句组成，每句五个字，总共二十个字。</strong></span>:heavy_exclamation_mark:</blockquote>"
            "您可以通过复制粘贴<br>"
            "<span style='color: #8B0000;'>帮我生成一首关于春的" + task + "绝句</span><br>"
            "到下面👇🏻的对话框，开启和小助理" + chatbot_name + "的对话。",
            unsafe_allow_html=True
        )

        # st.markdown("---")
    if user_input:
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        #============================================================================================================#  
        with st.chat_message("user"):
            # st.markdown(user_input)
            st.markdown("<span style='color: red;'>" + "您" + "：</span>" + user_input, unsafe_allow_html=True)
        
        
        with st.chat_message("assistant", avatar=chatbot_avatar):
            message_placeholder = st.empty()
            waiting_message = st.empty()  # Create a new placeholder for the waiting message
            dots = 0
            
            for dots in range(0, 5):
                dots = update_typing_animation(waiting_message, dots)  # Update typing animation
                time.sleep(0.2) 
            
        
            import time
            max_attempts = 2
            attempt = 0
            while attempt < max_attempts:
                try:
                    # raise Exception("test")    
                    message = client.beta.threads.messages.create(thread_id=st.session_state.thread_id,role="user",content=user_input)
                    import random
                    if len(st.session_state.messages) // 2 <= 1:
                        response = predefined_responses[(len(st.session_state.messages) // 2) - 1]
                    else:
                        response = random.choice(subsequent_responses)
                    message = client.beta.threads.messages.create(
                                thread_id=st.session_state.thread_id,
                                role="user",
                                content=response
                            )
                    waiting_message.empty()
                    message_placeholder.markdown("<span style='color: red;'>" + chatbot_name + "： </span><br>" + response, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    break
                except:
                    attempt += 1
                    if attempt < max_attempts:
                        print(f"An error occurred. Retrying in 5 seconds...")
                        time.sleep(3)
                    else:
                        error_message_html = """
                            <div style='display: inline-block; border:2px solid red; padding: 4px; border-radius: 5px; margin-bottom: 20px; color: red;'>
                                <strong>网络错误:</strong> 请重试。
                            </div>
                            """
                        full_response = error_message_html
                        waiting_message.empty()
                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
#============================================================================================================#  


        

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
