# step 1 
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

st.set_page_confi(layout = "wide")
#==================STEP 2 ENV AND API KEYS
st.title("Agentic PPT Generator")
st.header("""User can generate, ppt, Images, and fetch latest news""")
st.sidebar.title("Give API KEYS")
GOOGLE_API_KEY = st.sidebar.text_input("AQ.Ab8RN6I1v3B4s08tuzjuHlOx1ttdXKTSsgWK4hRGJUtk2uIdbQ")
TAVILY_API_KEY = st.sidebar.text_input("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")

ALL_API = [GOOGLE_API_KEY,TAVILY_API_KEY]
if not all(all_api):
  st.sidebar.error("Must pass ALL API-KEYS")
  url =  "https://aistudio.google.com/api-keys"
  st.markdown(f"Get Google AP key-{utl}")
  url ="https://app.tavily.com/playground"
  st.markdown(f"Get Tavilt AP key-{url}")


elif all(ALL_API):
  st.success("API KEYS LOADED")
  options = ["gemini-3.5-flash-lite","gemini-3.5-flash",
             "gemini-2.5-flash-lite","gemini-2.5-flash"]
  selected_model = st.selectbox("Select-Model",options = options)

  model = ChatGoogleGenerativeAI(
      model = 'gemini-3.5-flash-lite',
      google_api_key = GOOGLE_API_KEY
  )
  response=model.invoke("hello buddy!")
  response.content[-1]['text']
  
else:
  st.sidebar.info("Try Valid API-keys")

def search_latest_info(query):
  """This function helps to give latest search using tavily based on given user query related research or contents"""
  Client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = Client.search(query)
  return response

def generate_image(img_prompt,slide_no = 1):
  """This function helps user to generate image using free api,
  with given img_prompt, with slide no"""
  url = f"https://image.pollinations.ai/{img_prompt}"
  import requests as r
  content = r.get(url).content

  # Use a consistent filename for saving and opening
  filename = f"ai_image_{slide_no}.jpeg"

  with open(filename, 'wb') as f:
    f.write(content)
  return url

def run_agent(leader_agent, query):
    prompt = f"""Based on Below given Query,
    your task is to call specific tool, first to
    promptify user prompt, than call image tool, or
    latest search if required.give slide dynamic, ui ux,
    with creative design, keep help of function to generate image
    based on given topic,
    Generate image using
    with number of slide asked, and use time sleep to hit image request on server
    and using file handling embed this in output html, use java script function
    give Final response output in HTML, no markdowns
    user query given below:
    """

    prompt = prompt + query

    # prompt = agent_prompt(prompt)

    response = leader_agent.invoke({
        'messages': [{'role': 'user',
                'content': prompt}]})
    code = response['messages'][-1].content[-1]['text']
    return code

if all(ALL_API):
  leader_agent = create_agent(
    model = model,
    tools = [search_latest_info,
             #generate_image
             ])
  leader_agent
else:
 st.info("Give API-keys first to load Agent")


# ====================step 4 streamlit navbars=========================
tab1,tab2,tab3 = st.tabs(["Generate Image",
                          "Fetch News",
                          "Generate PPT"])
user_input = st.text_area("Write prompt & click enter")
if(user_input):
  with tab1:
    if st.button("Click to Generate Image"):
      with st.spinner("Running Agent"):
        try:
          url = generate_image(user_input)
          import requests as r
          img_data = r.get(url)
          st.image(url)
        except Exception as err:
          st.error("error Code:",err)
        
      
      with tab2:
        if st.button ("Fetch Latest News", key = "News-Button"):
          with st.spinner("Running Agent"):
            try:
              prompt = """Give Latest News Related to given user query in Dynamic html,
              output with cards Design Format. Strict HTML Output,
              No Any markdowns Response user Query: """ + user_input 
              response = leader_agent.invoke({'messages': [{'role': 'user',
                                                            'content': prompt}]})
              code = response['messages'][-1].content[-1]['text']
              st.html(code, width="stretch",unsafe_allow_javascript=true)
            
            except Exception as err:
              st.error("Error Code: ",err)
      with tab2:
        if st.button ("Click to Generate ppt", key = "PPT-Button"):
          with st.spinner("Running Agent"):
            try:
              code = run_agent(leader_agent,user_input)
              st.html(code, width="stretch",unsafe_allow_javascript=true)
              if st.download_button(label = "DOWNLOAD PPT",
                                    data = code,
                                    file_name = 'ppt.html',
                                    mime = 'text/html'):
                  st.success("PPT DOWNLOADED SUCCESSFULLY!!")
            except Exception as err:
              st.error("Error code: ",err)


