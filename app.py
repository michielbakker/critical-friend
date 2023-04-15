import streamlit as st
import openai
from datetime import datetime
from streamlit.components.v1 import html
import pandas as pd
import csv
st.set_page_config(page_title="Critical Friend")


html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="nainiayoub" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""


with st.sidebar:
    st.markdown("""
    # About 
    Critical friend is a helper tool built on GPT-3 to critique a statement.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work
    Simply enter your viewpoint and a critique of your viewpoint will be generated.
    You can also download the output as txt.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Made in the Music Room.
    """,
    unsafe_allow_html=True,
    )


input_text = None
if 'output' not in st.session_state:
    st.session_state['output'] = 0

if st.session_state['output'] <=2:
    st.markdown("""
    # Critical Friend
    """)
    input_text = st.text_input("Generate a critique in response to", disabled=False, placeholder="What's on your mind?")
    st.session_state['output'] = st.session_state['output'] + 1
else:
    # input_text = st.text_input("Brainstorm ideas for", disabled=True)
    st.info("Thank you! Refresh for more critiques💡")
    st.markdown('''
    <a target="_blank" style="color: black" href="https://twitter.com/intent/tweet?text=I%20just%20used%20the%20Critical%20Friend%20app!%0A%0Ahttps://michielbakker-critical-friend-app-lvizi2.streamlit.app/">
        <button class="btn">
            Tweet about this!
        </button>
    </a>
    <style>
    .btn{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: #fff;
        background-color: #00acee;
        width: auto;
        user-select: none;
        border: 1px solid #00acee;
        }
    .btn:hover{
        color: #00acee;
        background-color: #fff;
    }
    </style>
    ''',
    unsafe_allow_html=True
    )

hide="""
<style>
footer{
	visibility: hidden;
    position: relative;
}
.viewerBadge_container__1QSob{
    visibility: hidden;
}
#MainMenu{
	visibility: hidden;
}
<style>
"""
st.markdown(hide, unsafe_allow_html=True)

# html(button, height=70, width=220)
# st.markdown(
#     """
#     <style>
#         iframe[width="220"] {
#             position: fixed;
#             bottom: 60px;
#             right: 40px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
if input_text:
    if True:
        openai.api_key = st.secrets["openaiKey"]
        MODEL = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an assistant that helps people clarify their arguments. A user puts in a statement and you answer with a critique."},
                {"role": "user", "content": input_text},
                # {"role": "assistant", "content": "O hark! The hue of yonder fruit, it be the shade of an orange!"},
                # {"role": "user", "content": ""}
            ],
            temperature=0.8,
        )
        # response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)
        critique_output = response.choices[0].message.content
        today = datetime.today().strftime('%Y-%m-%d')
        topic = "Critique for: "+input_text+"\n@Date: "+str(today)+"\n"+critique_output
        
        st.info(critique_output)
        filename = "critical_friend_"+str(today)+".txt"
        btn = st.download_button(
            label="Download txt",
            data=topic,
            file_name=filename
        )
        fields = [input_text, critique_output, str(today)]
        # read local csv file
        r = pd.read_csv('./data/prompts.csv')
        if len(fields)!=0:
            with open('./data/prompts.csv', 'a', encoding='utf-8', newline='') as f:
                # write to csv file (append mode)
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(fields)

        
        

        
