from enum import Enum

class Color(Enum):
    RED = 'R'
    GREEN = 'G'
    BLUE = 'U'
    WHITE = 'W'
    BLACK = 'B'

class Query(Enum):
    INCLUDE = """
            WITH cosign_distance as (
                Select DISTINCT ON (name) c.name,
                c.oracle_text,
                c.type_line,
                c.identifiers->>'multiverseId' as img_id,
                e.embedding <=> %s::vector as distance
                From cards c
                    Inner Join oracle_embeddings e on c.oracle_hash = e.oracle_hash
                where c.identifiers->>'multiverseId' is not null AND c.color_identity @> %s
            ) Select name,
                oracle_text,
                img_id,
                type_line
            From cosign_distance
            ORDER BY distance 
            LIMIT %s OFFSET %s
        """
    EXCLUDE = """
            WITH cosign_distance as (
                Select DISTINCT ON (name) c.name,
                c.oracle_text,
                c.type_line,
                c.identifiers->>'multiverseId' as img_id,
                e.embedding <=> %s::vector as distance
                From cards c
                    Inner Join oracle_embeddings e on c.oracle_hash = e.oracle_hash
                where c.identifiers->>'multiverseId' is not null AND NOT (c.color_identity && %s)
            ) Select name,
                oracle_text,
                img_id,
                type_line
            From cosign_distance
            ORDER BY distance 
            LIMIT %s OFFSET %s
        """
    EXACTLY = """
            WITH cosign_distance as (
                Select DISTINCT ON (name) c.name,
                c.oracle_text,
                c.type_line,
                c.identifiers->>'multiverseId' as img_id,
                e.embedding <=> %s::vector as distance
                From cards c
                    Inner Join oracle_embeddings e on c.oracle_hash = e.oracle_hash
                where c.identifiers->>'multiverseId' is not null AND c.color_identity @> %s AND c.color_identity <@ %s
            ) Select name,
                oracle_text,
                img_id,
                type_line
            From cosign_distance
            ORDER BY distance 
            LIMIT %s OFFSET %s
        """