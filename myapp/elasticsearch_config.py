from elasticsearch import connections

def configure_elasticsearch():
    connections.configure(
        default={
            'hosts': ['http://127.0.0.1:9200'],  # Localhost and default Elasticsearch port
            'timeout': 30  # Optional timeout
        }
    )
