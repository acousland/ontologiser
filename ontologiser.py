import streamlit as st
import pandas as pd
from io import StringIO

st.markdown("# The Ontologiser  ", unsafe_allow_html=False, help=None)
st.markdown("_AI ontology extraction tool_", unsafe_allow_html=False, help=None)

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

    option = st.selectbox("Which column has your data in it?",list(dataframe.columns),placeholder="Select contact method...",)
    st.write('You selected:', option)

    st.slider('How many groups are you looking for?', 0, 25, 8)
    title = st.text_input('Any additional context for the AI to consider', '')

    modelType = st.selectbox("What kind of modelling are you doing?",("Data Modelling", 
                                                                      "Functional Modelling", 
                                                                      "Pain Point Identification",
                                                                      "Pain Point Theming"), placeholder="Select modelling type...",)
    
    if st.button("Generate domains", type="secondary"):
        st.write('Potatoes; Donkeys')

        st.graphviz_chart('''
        graph FAQ {
    node [shape=rectangle, style=filled, color=lightyellow]

    a [label="IM Health Check"]
    b [label="Duration"]
    c [label="Deliverables"]
    d [label="Benchmark Model"]
    e [label="Data Insights"]
    f [label="IM Systems Approach"]
    g [label="Architectural Framework"]
    h [label="Data Management"]
    i [label="Understanding Data"]
    j [label="Data Quality"]
    k [label="Business Benefits"]
    l [label="Compliance & Standards"]

    // Create edges to show the relations between different nodes
    a -- b
    a -- c
    a -- d
    a -- f
    b -- c
    c -- f
    d -- l
    e -- i
    e -- k
    f -- g
    f -- h
    f -- k
    g -- h
    h -- i
    h -- j
    i -- j
    j -- k
    k -- l
}
    }
''')

