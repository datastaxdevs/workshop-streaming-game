"""
    session.py
"""

import os
import atexit
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Credentials retrieval
load_dotenv()
try:
    SECURE_CONNECT_BUNDLE = os.environ['ASTRA_DB_SECURE_CONNECT_BUNDLE']
    USERNAME = os.environ['ASTRA_DB_USERNAME']
    PASSWORD = os.environ['ASTRA_DB_PASSWORD']
    KEYSPACE = os.environ['ASTRA_DB_KEYSPACE']
    #
    secure_connect_bundle = SECURE_CONNECT_BUNDLE
    path_to_creds = ''
    cluster = Cluster(
        cloud={
            'secure_connect_bundle': SECURE_CONNECT_BUNDLE
        },
        auth_provider=PlainTextAuthProvider(USERNAME, PASSWORD)
    )
    session = cluster.connect(KEYSPACE)

    # initialization of tables
    tableCreationResult = session.execute('''
        CREATE TABLE IF NOT EXISTS objects_by_game_id (
            game_id     UUID,
            kind        TEXT,
            object_id   UUID,
            "active"    BOOLEAN,
            x           INT,
            y           INT,
            h           BOOLEAN,
            generation  INT,
            name        TEXT,
            PRIMARY KEY ( (game_id), kind, object_id)
        ) WITH CLUSTERING ORDER BY (kind DESC, object_id DESC);
    ''')

    @atexit.register
    def shutdown_driver():
        cluster.shutdown()
        session.shutdown()

except KeyError:
    raise KeyError('Environment variables not detected. Perhaps you forgot to '
                   'prepare the .env file ?')
