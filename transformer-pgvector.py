#!/usr/bin/env python3

# https://github.com/pgvector/pgvector-python/blob/master/examples/sentence_embeddings.py
# https://github.com/pgvector/pgvector-python/blob/master/examples/openai_embeddings.py
# https://github.com/pgvector/pgvector-python/blob/master/examples/sentence_embeddings.py
#
# Vector Databases
# https://www.youtube.com/watch?v=YU66YlZW6dA
# https://youtu.be/E4ot5d79jdA

import argparse
import psycopg
import warnings
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

def setup_database(_connection, _vector_dimension, _databaseSetup: bool = True) -> None:
    """
    Note:
    psql postgres
    CREATE DATABASE pgvector_example;
    """
    if not _databaseSetup:
        return

    print("Info: Setting up Database")

    _connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
    _connection.execute("DROP TABLE IF EXISTS documents")
    _connection.execute(
        """
        CREATE TABLE documents (
            id bigserial PRIMARY KEY,
            content text,
            embedding vector(%s)
        )"""
        % _vector_dimension)
    # https://aiven.io/developer/postgresql-pgvector-indexes
    # for large datasets
    # _connection.execute("CREATE INDEX idx_content_ivfflat ON documents USING ivfflat (embedding vector_l2_ops) WITH (lists = 3)")
    # _connection.execute("CREATE INDEX idx_content_ivfflat ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10)")
    # _connection.execute("CREATE INDEX idx_content_hnsw ON documents USING hnsw (embedding vector_l2_ops) WITH (m = 10, ef_construction = 40)")

def upload_corpus(
    _corpus: list[str],
    _model,
    _connection,
    _convert_to_tensor: bool = False,
    _databaseSetup: bool = True,
) -> None:
    if not _databaseSetup:
        return

    print("Info: Uploading corpus")

    corpus_embeddings = _model.encode(
        _corpus, convert_to_tensor=_convert_to_tensor, normalize_embeddings=True
    )

    for content, embedding in zip(_corpus, corpus_embeddings):
        _connection.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding),
        )


def get_connection():
    conn = psycopg.connect(dbname="pgvector_example", autocommit=True)
    register_vector(conn)
    return conn


###############################################################################
#
# SEMANTIC QUERY
#
###############################################################################

vector_dimension = 1024

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
    )
    # https://huggingface.co/spaces/mteb/leaderboard
    # https://huggingface.co/intfloat/multilingual-e5-large-instruct

    # Test model poor performance
    # model = SentenceTransformer(
    #     "mixedbread-ai/mxbai-embed-large-v1", truncate_dim=vector_dimension
    # )

    # Reference model
    model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

convert_to_tensor: bool = False
databaseSetup: bool = False
pg_conn = get_connection()

parser = argparse.ArgumentParser()
parser.add_argument('--database-setup', action='store_true', help='Setup the database')
args = parser.parse_args()
databaseSetup: bool = args.database_setup

setup_database(
    _connection=pg_conn, _vector_dimension=vector_dimension, _databaseSetup=databaseSetup
)

corpus = [
    "Princess Leia hides the Death Star plans in R2-D2.",
    "Darth Vader captures Princess Leia's ship.",
    "Luke Skywalker discovers a message from Princess Leia in R2-D2.",
    "Luke meets Obi-Wan Kenobi and learns about the Force.",
    "Luke's aunt and uncle are killed by Imperial stormtroopers.",
    "Luke and Obi-Wan hire Han Solo and Chewbacca at Mos Eisley Cantina.",
    "The Millennium Falcon escapes Tatooine and is pursued by Imperial ships.",
    "The Millennium Falcon is captured by the Death Star.",
    "Luke, Han, and Chewbacca rescue Princess Leia.",
    "They escape through the garbage chute and are nearly crushed.",
    "Obi-Wan Kenobi disables the tractor beam.",
    "Obi-Wan Kenobi duels Darth Vader and sacrifices himself.",
    "The Millennium Falcon escapes from the Death Star.",
    "R2-D2 delivers the Death Star plans to the Rebel Alliance.",
    "The Rebels plan an attack on the Death Star.",
    "Luke joins the Rebel fleet as a pilot.",
    "The Rebels begin their attack on the Death Star.",
    "Han Solo returns to help Luke during the attack.",
    "Luke uses the Force to destroy the Death Star.",
    "The Rebels celebrate their victory and honor their heroes.",
    "The Rebels are stationed on the ice planet Hoth.",
    "Imperial forces discover the Rebel base and attack.",
    "Han Solo and Princess Leia escape in the Millennium Falcon.",
    "Luke Skywalker travels to Dagobah to train with Yoda.",
    "Han and Leia evade the Empire and hide in Cloud City.",
    "Darth Vader reveals a trap to capture Luke.",
    "Han Solo is betrayed and frozen in carbonite.",
    "Luke confronts Vader and loses his hand in a lightsaber duel.",
    "Vader reveals that he is Luke's father.",
    "Luke escapes with the help of Leia, Lando, and Chewbacca.",
    "Luke Skywalker and his friends plan to rescue Han Solo.",
    "They infiltrate Jabba the Hutt's palace on Tatooine.",
    "Leia frees Han, but they are captured.",
    "Luke arrives and defeats Jabba's forces.",
    "The group destroys Jabba's sail barge and escapes.",
    "The Rebels plan an attack on the new Death Star.",
    "Luke returns to Dagobah to complete his training.",
    "Yoda dies, and Luke learns Leia is his sister.",
    "The Rebels land on Endor to disable the Death Star's shield generator.",
    "Luke surrenders to Vader to confront the Emperor.",
    "Vader takes Luke to the Emperor on the Death Star.",
    "The Rebels attack the Death Star while ground forces fight on Endor.",
    "Luke refuses to join the dark side and battles Vader.",
    "Vader turns on the Emperor to save Luke.",
    "Vader dies, and the Death Star is destroyed.",
    "The Empire is defeated, and the galaxy celebrates.",
]

upload_corpus(
    _corpus=corpus,
    _model=model,
    _connection=pg_conn,
    _convert_to_tensor=convert_to_tensor,
    _databaseSetup=databaseSetup,
)

# https://github.com/pgvector/pgvector-python/blob/master/examples/hybrid_search_rrf.py
sql = """
WITH semantic_search AS (
    SELECT id, content, RANK () OVER (ORDER BY embedding <=> %(embedding)s) AS rank
    FROM documents
    ORDER BY embedding <=> %(embedding)s
    LIMIT 100
)

SELECT semantic_search.id AS id,
       semantic_search.content AS content,
       semantic_search.rank as rank
FROM semantic_search
ORDER BY rank ASC
LIMIT 10
"""

query = "Tell me about Princess Leia!"
query = "Was ist passiert?"
query = "Was weisst du über Prinzessinnen?"
query = "How are they related to each other?"
query = "Was weisst du über Armeen?"
query = "Wer ist mit wem verwandt?"
query_embedding = model.encode(
    query, convert_to_tensor=convert_to_tensor, normalize_embeddings=True
)

results = pg_conn.execute(
    sql, {"query": query, "embedding": query_embedding}
).fetchall()

print("=" * (len("Query: ") + len(query)))
print("Query:", query)
print("=" * (len("Query: ") + len(query)))

for row in results:
    # print("Document ID:", row[0], "Content:", row[1], "Rank:", row[2])
    print(row[1])
