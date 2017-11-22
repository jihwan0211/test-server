from datetime import datetime, timezone

import pytz
import json

from flask import request
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from model.news import NewsDataListModel, PostNewsDataModel
from flask_restful.representations.json import output_json
#from endpoint import output_json
from controller.database import DatabaseConnector

import config
#for debug
import pdb

class PostNewsData(Resource):
    @swagger.doc({
        'description': '뉴스 데이터 게시',
        'tags': ['news-data'],
        'parameters': [
            {
                'name': 'body', 'in': 'body',
                'description': '뉴스 내용',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        "title": {"type": "string"},
                        "contents": {"type": "string"},
                        "url": {"type": "string"}
                    },
                    'example': PostNewsDataModel().data
                }
            }
        ],
        'responses': {
            '200': {
                'description': '뉴스 데이터 게시 완료',
                'examples': {
                    'application/json': {
                        "message": 'ok',
                        "post_uid": 0
                    }
                }
            },
            '400': {
                'description': 'param error',
                'examples': {
                    'application/json': config.BAD_REQUEST
                }
            },
            '424': {
                'description': '뉴스 데이터 게시 실패',
                'examples': {
                    'application/json': config.FAILURE
                }
            },
            '500': {
                'description': 'server internal error',
                'examples': {
                    'application/json': config.UNKNOWN_ERROR
                }
            }
        }
    })

    def post(self):
        """뉴스 데이터 게시"""
        try:
            args = request.get_json()
            title = args.get('title')
            contents = args.get('contents')
            url = args.get('url')

            if title is None:
                return output_json(config.BAD_REQUEST, 400)
            else:
                dbc = DatabaseConnector()
                reth_number = dbc.post_news_data(title, contents, url)

                if reth_number is not False:
                    return output_json({
                        "message": 'ok',
                        "nid": reth_number
                    }, 200)
                else:
                    return output_json(config.FAILURE, 424)
        except Exception as ex:
            return output_json({
                "message": str(type(ex)) + " / " + str(ex)
            }, 500)


class NewsDataList(Resource):
    @swagger.doc({
        'description': '뉴스 데이터',
        'tags': ['news-data'],
        'parameters': [
            {
                "name": "page", "type": "integer", 'in': 'path', 'required': True,
                "description": "페이지 번호"
            }
        ],
        'responses': {
            '200': {
                'description': '뉴스 목록',
                'examples': {
                    'application/json': {
                        "message": "ok",
                        "page": 1,
                        "news": [
                            NewsDataListModel().data
                        ]
                    }
                }
            },
            '204': {
                'description': '뉴스 데이터 없음',
                'examples': {
                    'application/json': {
                        "message": "no data"
                    }
                }
            }
        }
    })
    def get(self, page):
        """뉴스 데이터"""
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int)

        if page.isnumeric() is False or int(page) <=0:
            return output_json(config.BAD_REQUEST, 400)

        # 데이터 베이스 커넥터
        dbc = DatabaseConnector()
        news_datas = dbc.get_news_data(int(page), 50)
        
        #result_new_data = []
        
        # 가공이 필요 할 시
        #for row in news_datas:

        if news_datas is not None and len(news_datas) > 0:
            return {
                "message": "ok",
                "page":page,
                "data":news_datas
            }
        else:
            return output_json({
                "message": "no data"
            }, 204)

class UpdateNewsData(Resource):
    @swagger.doc({
        'description': '뉴스 데이터 수정',
        'tags': ['news-data'],
        'parameters': [
            {
                "name": "nid", "type": "integer", 'in': 'path', 'required': True,
                "description": "글 번호"
            },
            {
                'name': 'body', 'in': 'body',
                'description': '뉴스 내용',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        "title": {"type": "string"},
                        "contents": {"type": "string"},
                        "url": {"type": "string"}
                    },
                    'example': PostNewsDataModel().data
                }
            }
        ],
        'responses': {
            '200': {
                'description': '뉴스 데이터 게시 완료',
                'examples': {
                    'application/json': {
                        "message": 'ok',
                        "post_uid": 0
                    }
                }
            },
            '304': {
                'description': '수정된 내용 없음',
                'examples': {}
            },
            '400': {
                'description': 'param error',
                'examples': {
                    'application/json': config.BAD_REQUEST
                }
            },
            '401': {
                'description': '권한 없음',
                'examples': {
                    'application/json': config.UNAUTHORIZED
                }
            },
            '424': {
                'description': '뉴스 데이터 수정 실패',
                'examples': {
                    'application/json': config.FAILURE
                }
            },
            '500': {
                'description': 'server internal error',
                'examples': {
                    'application/json': config.UNKNOWN_ERROR
                }
            }
        }
    })
    def put(self, nid):
        """뉴스 데이터 수정"""
        try:
            if nid.isnumeric() is False or int(nid) <= 0:
                return output_json(config.BAD_REQUEST, 400)

            args = request.get_json()
            title = args.get('title')
            contents = args.get('contents')
            url = args.get('url')

            if title is None:
                return output_json(config.BAD_REQUEST, 400)
            else:
                dbc = DatabaseConnector()
                reth_number = dbc.update_news_data(nid, title, contents, url)

                if reth_number == -2:
                    return output_json(config.NOT_MODIFIED, 304)
                elif reth_number == -1:
                    return output_json(config.FAILURE, 424)
                elif reth_number is False:
                    return output_json(config.UNAUTHORIZED, 401)
                else:
                    return output_json(config.OK, 200)
        except Exception as ex:
            return output_json({
                "message": str(type(ex))+" / "+str(ex)
            }, 500)
        
class RemoveNewsData(Resource):
    @swagger.doc({
        'description': '뉴스 데이터 삭제',
        'tags': ['news-data'],
        'parameters': [
            {
                "name": "nid", "type": "integer", 'in': 'path', 'required': True,
                "description": "글 번호"
            }
        ],
        'responses': {
            '200': {
                'description': '포스트 삭제 완료',
                'examples': {
                    'application/json': config.OK
                }
            },
            '400': {
                'description': 'param error',
                'examples': {
                    'application/json': config.BAD_REQUEST
                }
            },
            '401': {
                'description': '권한 없음',
                'examples': {
                    'application/json': config.UNAUTHORIZED
                }
            },
            '500': {
                'description': 'server internal error',
                'examples': {
                    'application/json': config.UNKNOWN_ERROR
                }
            }
        }
    })
    def delete(self, nid):
        """ 뉴스 데이터 삭제 """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nid', type=int)

            if nid is None or int(nid) <= 0:
                return output_json(config.BAD_REQUEST, 400)

            dbc = DatabaseConnector()
            result = dbc.remove_news_data(nid)

            if result is True:
                return output_json(config.OK, 200)
            else:
                return output_json(config.UNAUTHORIZED, 401)
        except Exception as ex:
            return output_json({
                "message": str(type(ex))+" / "+str(ex)
            }, 500)

            
        
        