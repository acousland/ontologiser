from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import openai
import streamlit as st
import pandas as pd
from io import StringIO
import math

if openai.api_key not in st.session_state:
  openai.api_key = st.secrets["OPENAI_API_KEY"]


modelling_type = {"Data Entities": "I want you to find out what the key entities would be if this data was going to be represented in a relational database",
                  "Functions": "I want you to find out what the key functions would be if this data was going to be used to develop a Porters Value Chain",
                  "Systems": "I want you to find out all the systems and platforms that are mentioned",
                  "Pain Points": "I want you to find out what the key pain points would be that are hurting the organiastion. Focus on risks and inefficiencies"}


output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="""I'm going to present you with a list of values \\
    I want you to identify {number} AND ONLY {number} key {subject} that would represent these values \\
    {content_instructions}
    {additional_prompts}
    format them according to: {format_instructions} \\
    Make sure you only return a single entity per list item.
    The values are as follows:
    {data}
    
    """,
    input_variables=["number", "subject", "content_instructions", "additional_prompts", "data"],
    partial_variables={"format_instructions": format_instructions}
)

model = OpenAI()

st.markdown("# The Ontologiser  ", unsafe_allow_html=False, help=None)
st.markdown("_AI ontology extraction tool_", unsafe_allow_html=False, help=None)

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

    option = st.selectbox("Which column has your data in it?",list(dataframe.columns),placeholder="Select contact method...",)
    st.write('You selected:', option)

    groups = st.slider('How many groups are you looking for?', 0, 25, 8)
    prompts = st.text_input('Any additional context for the AI to consider', '')

    modelType = st.selectbox("What kind of modelling are you doing?",list(modelling_type.keys()), placeholder="Select modelling type...",)
    
    if st.button("Generate domains", type="secondary"):
        _input = prompt.format(number = groups, 
                               subject=modelType, 
                               content_instructions = modelling_type[modelType], 
                               additional_prompts = prompts,
                               data=dataframe[option])
        output = model(_input)
        st.write(output_parser.parse(output))