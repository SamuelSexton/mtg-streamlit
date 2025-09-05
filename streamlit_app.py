import streamlit as st
from embeddings_model import load_embedding_model
from embedding_db import Embedding_Db
import time

IMG_URL = "https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="
start_time = time.perf_counter()
model = load_embedding_model()
total_time = time.perf_counter() - start_time

st.title("MTG card search with symantic search support.")

st.header("Coming Soon:")
st.write("""Search function with all the regular searches that 
         you are familiar with along with symatic search support.""")

db = Embedding_Db()

query = st.text_input("Symantic Search", placeholder="Type in a sentence or two of what you want your card to do.")
if query:
    embedding = model.encode(query, prompt_name="query").tolist()
    rows = db.get_cosign(embedding, limit=5)
    for row in rows:
        img_col, info_col = st.columns(2, border=True)
        img_col.image("https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="+row['img_id'], width=250)
        with info_col:
            st.subheader(row['name'])
            type_line = row['type_line']
            st.write(type_line)
            st.write(row['oracle_text'])
    st.write("-----------------------------")


