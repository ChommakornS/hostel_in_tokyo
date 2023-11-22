from flask import Flask, request
from markupsafe import escape
from flask import render_template
from elasticsearch import Elasticsearch
import math

ELASTIC_PASSWORD = "Harukyu0004"

es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    page_size = 9
    keyword = request.args.get('keyword')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no - 1),
        'query': {
            'bool': {
                'should': [
                    {
                        'match': {
                            'hostel.name': {
                                'query': keyword,
                                'fuzziness': 'auto',
                                'boost': 2,  # Boost the importance of matching hostel names
                                "fuzzy_transpositions": 'true'
                            }
                        }
                    },
                    {
                        'match': {
                            'hotel description': {
                                'query': keyword,
                                'fuzziness': 'auto',
                                'boost': 1,  # Lower boost for matching hotel descriptions
                                "fuzzy_transpositions": 'true'

                            }
                        }
                    }
                ]
            }
        }
    }

    res = es.search(index='hostelindex', body=body)

    hits = [{'hostel.name': doc['_source']['hostel.name'], 'hotel description': doc['_source']['hotel description'], 'price.from': doc['_source']['price.from'], 
    'Link discord': doc['_source']['Link discord'],'Distance':doc['_source']['Distance'],'_id':doc['_id']} for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html',keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)

@app.route('/detail/<string:hostel_id>')
def detail(hostel_id):
    try:
        # Fetch details from Elasticsearch based on the _id
        res = es.get(index='hostelindex', id=hostel_id)

        # Extract relevant information from the Elasticsearch response
        hostel_details = {
            'hostel_name': res['_source']['hostel.name'],
            'price_from': res['_source']['price.from'],
            'description': res['_source']['hotel description'],
            'link_discord': res['_source']['Link discord'],
            'distance': res['_source']['Distance'],
            'rating': res['_source']['summary.score'],  # Add rating field
        }
        return render_template('detail.html', hostel_details=hostel_details)

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        # Return an error page or handle the error appropriately
        return render_template('error.html', error_message='An error occurred while fetching hostel details.')


