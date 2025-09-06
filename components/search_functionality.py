import streamlit as st


def search_area():
    with st.form("search_form"):
        text = st.text_input("Symantic Search", placeholder="Type in a sentence or two of what you want your card to do.")
        submitted = st.form_submit_button("Search")
        if submitted and text:
            return {'query': text}
        return {'query': None}

def get_query_results(query, model, db, limit, offset):
    if query['query']:
        embedding = model.encode(query['query'], prompt_name="query").tolist()
        rows = db.get_cosign(embedding, limit, offset)
        for row in rows:
            img_col, info_col = st.columns(2, border=True)
            img_col.image("https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="+row['img_id'], width=250)
            with info_col:
                st.subheader(row['name'])
                type_line = row['type_line']
                st.write(type_line)
                st.write(row['oracle_text'])
        return rows