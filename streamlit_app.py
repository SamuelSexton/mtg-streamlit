import streamlit as st
from components.search_functionality import search_area, get_query_results
from embeddings_model import load_embedding_model
from embedding_db import Embedding_Db
import time

# def search_area():
#     with st.form("search_form"):
#         text = st.text_input("Symantic Search", placeholder="Type in a sentence or two of what you want your card to do.")
#         submitted = st.form_submit_button("🔍 Search")
#         if submitted and text:
#             return {'query': text}
#         return {'query': None}

IMG_URL = "https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="
start_time = time.perf_counter()
model = load_embedding_model()
total_time = time.perf_counter() - start_time

st.title("MTG card search with symantic search support.")

st.header("Coming Soon:")
st.write("""Search function with all the regular searches that 
         you are familiar with along with symatic search support.""")

db = Embedding_Db()
st.session_state['next'] = 0
filters = search_area()
rows = get_query_results(filters, model, db, limit=10, offset=0)
if st.session_state['FormSubmitter:search_form-Search'] == True:
    st.session_state['filters'] = filters
    st.session_state['results'] = rows
    st.session_state['next'] = 10

try:
    if st.button('Next Results'):
        if st.session_state['filters']:
            print("clicked")
            next_set = st.session_state['next']
            get_query_results(st.session_state["filters"], model, db,limit=10, offset=next_set)
            st.session_state['next'] += 10
            print(st.session_state['next'])
except Exception as e:
    st.write("Please Complete a Search first before trying to find the next results of nothing.")




