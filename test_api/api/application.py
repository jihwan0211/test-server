from flask import Flask
from flask_restful_swagger_2 import Api

from endpoint.news import *

APP = Flask(__name__)
APP.secret_key = '7ZWY7JmA7JygIOyEuOyFmCDslZTtmLjtmZQg7YKk44Gv44O844KP44O844KG44GF44O844GE44KT44GP44KK44Gj44G344GX44KH44KT44GN44O8'
APP.config['SESSION_TYPE'] = 'filesystem'

API = Api(APP, title='test_api', api_version='0.0.1', api_spec_url='/api/swagger', host='localhost', description='Test Restful API')

API.add_resource(PostNewsData, '/news')
API.add_resource(NewsDataList, '/news/<page>')
API.add_resource(UpdateNewsData, '/news/<nid>')
API.add_resource(RemoveNewsData, '/news/<nid>')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, threaded=True)