from opensearchpy import OpenSearch

host = 'localhost'
port = 9200


host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
ca_certs_path = '/etc/ssl/certs' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)

index_name = 'python-test-index_1'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print(response)