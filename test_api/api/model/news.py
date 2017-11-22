class NewsDataListModel:
    nid=0
    title='title name'
    contents='contents'
    url='news.naver.com'
    timestamp='2017-11-14 00:00:00'

    def __init__(self):
        pass

    @property
    def data(self):
        return {
            "nid":self.nid,
            "title":self.title,
            "contents":self.contents,
            "url":self.url,
            "timestamp":self.timestamp
        }

class PostNewsDataModel:
    title=''
    contents=''
    url=''
    
    def __init__(self):
        pass

    @property
    def data(self):
        return {
            "title": self.title,
            "contents": self.contents,
            "url": self.url
        }


class UpdateNewsDataModel:
    nid = 0    
    title = ''
    contents = ''
    url = ''

    def __init__(self):
        pass

    @property
    def data(self):
        return {
            "nid": self.nid,
            "title": self.title,
            "contents": self.contents,
            "url": self.url
        }
