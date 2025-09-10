import streamlit as st


def search_area():
    with st.form("search_form"):
        mode = st.selectbox('Filter by Commander Color Identity',
                 ['Include', 'Exactly', 'Exclude'], key='commander_identity')
        cols = st.columns(5)
        with cols[0]:
            blue=st.checkbox('Blue', key='blue')
        with cols[1]:
            black=st.checkbox('Black', key='black')
        with cols[2]:
            white=st.checkbox('White',key='white')
        with cols[3]:
            red=st.checkbox('Red', key='red')
        with cols[4]:
            green=st.checkbox('Green',key='green')
        text = st.text_input("Symantic Search", placeholder="Type in a sentence or two of what you want your card to do.")
        submitted = st.form_submit_button("Search")
        colors = []
        if submitted and text:
            if blue: colors.append("U")
            if black: colors.append("B")
            if white: colors.append("W")
            if red: colors.append("R")
            if green: colors.append("G")

            return {
                'query': text,
                'mode': mode,
                'colors': colors,
                'submitted': True
            }
        return {
            'query': None,
            'mode': mode,
            'colors': colors,
            'submitted': False
            }

def get_query_results(filters, model, db, limit, offset):
    if filters['query']:
        embedding = model.encode(filters['query'], prompt_name="query").tolist()
        rows = db.get_cosign_filtered(embedding, filters, limit, offset)
        for row in rows:
            img_col, info_col = st.columns(2, border=True)
            img_col.image("https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="+row['img_id'], width=250)
            with info_col:
                st.subheader(row['name'])
                type_line = row['type_line']
                st.write(type_line)
                st.write(row['oracle_text'])
        return rows