from elasticsearch import Elasticsearch, helpers
import ndjson
import argparse
import uuid
import chardet
import certifi

# python elasticsearch_loader.py --file hoteldataset.json --index hostelindex
es = Elasticsearch("https://localhost:9200", 
	http_auth = ("elastic", "Harukyu0004"),
	scheme = "https", port = 443, maxsize = 5,
          use_ssl=True, ca_certs=certifi.where(), verify_certs=False)

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--index')
# parser.add_argument('--type')

args = parser.parse_args()

index = args.index
file = args.file
# doc_type = args.type


with open('hosteldataset.json', 'r', encoding='utf-8') as json_file:
    json_docs = ndjson.load(json_file)

with open('hosteldataset.json', 'rb') as rawdata:
    result = chardet.detect(rawdata.read())
    encoding = result['encoding']

with open('hosteldataset.json', 'r', encoding=encoding) as json_file:
    json_docs = ndjson.load(json_file)

def bulk_json_data(json_list, _index):
    for doc in json_list:
        yield {
            "_index": _index,
            "_id": str(uuid.uuid4()),  # Convert UUID to string
            "_source": doc
        }

try:
    response = helpers.bulk(es, bulk_json_data(json_docs, index))
    print ("\nRESPONSE:", response)

except Exception as e:
    print("\nERROR:", e)
