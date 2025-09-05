import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0')