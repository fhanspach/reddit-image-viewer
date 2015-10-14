import datetime
import requests
import time
from reddit_api.models import Reddit
from django.conf import settings

HEADER = {"User-Agent": settings.REDDIT_API_USER_AGENT}


class RedditImporter(object):
    def __init__(self):
        self.last_request = datetime.datetime.now()
        self.after = None

    def _save_reddit(self, reddit):
        new_reddit, _ = Reddit.objects.update_or_create(
            url=reddit['url'],
            defaults={
                "title": reddit['title'],
                "display_name": reddit['display_name'],
                "description": reddit['description'],
                "over18": reddit['over18'],
                "public_description": reddit['public_description'],
                "date_created": datetime.datetime.fromtimestamp(reddit['created']),
                "subscribers": reddit['subscribers'],
                "banner_image": reddit['banner_img']}
        )
        new_reddit.save()
        print(new_reddit.title)

    def _send_request(self, url):
        # prevent that there are more requests than every 3 seconds
        if self.last_request - datetime.datetime.now() < datetime.timedelta(seconds=3):
            time.sleep(3)
        response = requests.get(url, headers=HEADER)
        response_json = response.json()
        if response.status_code == 429:
            time.sleep(30)
            return self._send_request(url)

        self.last_request = datetime.datetime.now()
        return response_json

    def import_single_reddit(self, url):
        if not url.endswith("/"):
            url += "/"

        url = settings.REDDIT_ABOUT.format(url)
        response_json = self._send_request(url)
        self._save_reddit(response_json['data'])

    def import_all_reddits(self):
        print("import started: {}".format(self.after))

        url = settings.ALL_REDDITS_URL.format(settings.IMPORT_BATCH_SIZE,
                                              "&after={}".format(self.after) if self.after else "")
        response_json = self._send_request(url)

        for reddit_data in response_json['data']['children']:
            reddit_data = reddit_data['data']
            self._save_reddit(reddit_data)

        self.after = response_json['data']['after']
        if self.after == "" or self.after is None:
            return
        self.import_all_reddits()
