import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from mtg_enums import Query

@st.cache_resource
class Embedding_Db():

    def __init__(self):
        self.connect()
    
    def test_connection(self) -> bool:
            if self.conn.closed == 0:
                print("Connected")
                return True
            else:
                print("Disconnected. Reconnect to resume DB operations")
                return False
            
    def connect(self) -> None:
        try:
            if st.secrets:
                self.conn = psycopg2.connect(
                    st.secrets['db']["conn_string"]
                )
                self.conn.set_client_encoding('UTF8')
        except Exception as e:
            load_dotenv()
            self.conn = psycopg2.connect(
                os.getenv("AIVEN_DB")
            )
            self.conn.set_client_encoding('UTF8')

    def disconnect(self) -> None:
        self.conn.close()
        print('Database has been closed.')
    
    # def get_cosign(self, embedding,limit=10, offset=0):
    #     stmt = """
    #         WITH cosign_distance as (
    #             Select DISTINCT ON (name) c.name,
    #             c.oracle_text,
    #             c.type_line,
    #             c.identifiers->>'multiverseId' as img_id,
    #             e.embedding <=> %s::vector as distance
    #             From cards c
    #                 Inner Join oracle_embeddings e on c.oracle_hash = e.oracle_hash
    #             where c.identifiers->>'multiverseId' is not null
    #         ) Select name,
    #             oracle_text,
    #             img_id,
    #             type_line
    #         From cosign_distance
    #         ORDER BY distance 
    #         LIMIT %s OFFSET %s
    #     """
    #     try:
    #         with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
    #             cursor.execute(stmt, (embedding,limit,offset))
    #             rows = cursor.fetchall()
    #             return rows
    #     except psycopg2.Error as e:
    #         print(f"Database error: {e}")
    #         return []

    def get_params(self, embedding, filters, limit, offset):
        params = [embedding, filters['colors']]

        if filters['mode'] == 'Exactly':
            params.append(filters['colors'])
        
        params.append(limit)
        params.append(offset)
        return params

    def get_cosign_filtered(self,embedding, filters, limit, offset):
        stmt = ''
        match filters['mode']:
            case 'Exactly':
                stmt = Query.EXACTLY.value
            case 'Include':
                stmt = Query.INCLUDE.value
            case 'Exclude':
                stmt = Query.EXCLUDE.value
        params = self.get_params(embedding, filters, limit, offset)
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(stmt, params)
                rows = cursor.fetchall()
                return rows
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_img_id():
        stmt = """
            Select identifiers->>'multiverseId' as img_id,
            From cards
            Where uuid IN(%s)
            LIMIT %s OFFSET 0
        """
        pass