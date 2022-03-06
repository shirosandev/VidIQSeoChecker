import json
import requests
from pytube import YouTube

class GetSeo(object):


    def __init__(self, video_link : str) -> None:
        self.tags : list = []
        self.seo : float = 0
        self.tags_position : list = []
        self.video_description : str = ""
        self.video_title : str = ""
        self.video_id : str = ""

        self.video_link : str = video_link

        self.__get_video_id()
        self.__get_video_info()
        self.__get_video_position()
        self.__get_video_seo()

    def __get_video_id(self) -> None:
        """Метод получения id видео
        """
        # TODO: Впилить больше случаев/найти другой метод получения id.
        self.video_id = self.video_link\
            .replace("https://", "")\
            .replace("www.youtube.com/watch?v=", "")\
            .replace("youtu.be/","")\
            .replace("youtube.com/watch?v=","")
        if "&" in self.video_id:
            self.video_id = self.video_id.split("&")[0]

    def __get_video_info(self) -> None:
        """Метод получения названия, тегов и описания видео.
        """
        yt = YouTube(self.video_link)
        self.video_description = yt.description
        self.video_title = yt.title
        self.tags = yt.keywords

    def __get_video_position(self):
        """Получение позиции видео по тегам.
        Используется сервис https://ytrank-legacy.vercel.app
        """
        link = "https://ytrank-legacy.vercel.app/graphql"
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '735',
            'content-type': 'application/json',
            'origin': 'https://ytrank.net',
            'referer': 'https://ytrank.net/',
            'sec-ch-ua': '"Opera GX";v="81", " Not;A Brand";v="99", "Chromium";v="95"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61'
        }
        payload = {"operationName":"youtubeVideoRank",
        "variables":{"videoId":self.video_id,"keywords":self.tags,"regionCode":"US"},
        "query":"query youtubeVideoRank($videoId: ID!, $keywords: [String], $regionCode: String) {\n  youtubeVideoRank(videoId: $videoId, keywords: $keywords, regionCode: $regionCode) {\n    ...VideoDetail\n    regionCode\n    keywords {\n      keyword\n      rank {\n        date\n        found\n"\
            "        page\n        position\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VideoDetail on YoutubeVideo {\n  videoId\n  title\n  publishedAt\n"\
            "  description\n  channelId\n  channelTitle\n  thumbnails {\n    small\n    medium\n    large\n    __typename\n  }\n  tags\n  __typename\n}\n"}
        result = requests.post(link, data=json.dumps(payload), headers=headers).text
        result = json.loads(result)['data']['youtubeVideoRank']['keywords']
        position : int = 0 
        for tag in result:
            if not tag['rank'][0]['found']:
                self.tags_position.append({'text' : tag['keyword']})
                continue
            if tag['rank'][0]['page'] > 1:
                position = tag['rank'][0]['page'] * 10 + tag['rank'][0]['position']

            else:
                position = tag['rank'][0]['position']
            self.tags_position.append({'search_rank' : position,'text' : tag['keyword']})
    
    def __get_video_seo(self):
        headers = {
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61'
        }
        payload = {
            "client" : "3.65.0",
            "country" : "US",
            "description" : str(self.video_description.encode('ascii', errors='ignore')),
            "language" : "en",
            "tags" : self.tags_position,
            "title" : str(self.video_title.encode('ascii', errors='ignore'))

        }
        result = requests.post('https://app.vidiq.com/v2/youtube_seo_score', headers=headers, data=json.dumps(payload))
        self.seo = json.loads(result.text)['overall']



