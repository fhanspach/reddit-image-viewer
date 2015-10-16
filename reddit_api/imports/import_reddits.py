import datetime
import pytz
import requests
import time
from reddit_api.models import Reddit
from django.conf import settings

HEADER = {"User-Agent": settings.REDDIT_API_USER_AGENT}

REDDIT_COLOR = '\033[94m'
REDDIT_COLOR_RED = '\033[1;35m'


class RedditImporter(object):
    def __init__(self):
        self.last_request = None
        self.after = None

    def _save_reddit(self, reddit_dict):
        reddit, created = Reddit.objects.update_or_create(
            url=reddit_dict['url'],
            defaults={
                "title": reddit_dict['title'],
                "display_name": reddit_dict['display_name'],
                "description": reddit_dict['description'],
                "over18": reddit_dict['over18'],
                "public_description": reddit_dict['public_description'],
                "date_created": datetime.datetime.fromtimestamp(reddit_dict['created'], tz=pytz.UTC),
                "subscribers": reddit_dict['subscribers'],
                "banner_image": reddit_dict['banner_img']}
        )
        reddit.save()
        log_string = "{} {}{}\033[0m({})".format('n' if created else 'u',
                                                 REDDIT_COLOR_RED if reddit.over18 else REDDIT_COLOR, reddit.url,
                                                 reddit.subscribers)
        print(log_string)
        return reddit

    def _wait_if_required(self):
        # prevent that there are more requests than every 3 seconds
        if self.last_request is not None \
                and self.last_request - datetime.datetime.now() < datetime.timedelta(seconds=3):
            time.sleep(3)

    def _send_request(self, url):
        self._wait_if_required()
        response = requests.get(url, headers=HEADER)
        response_json = response.json()
        if response.status_code == 429:
            time.sleep(30)
            return self._send_request(url)
        response.raise_for_status()

        self.last_request = datetime.datetime.now()
        return response_json

    def import_single_reddit(self, url):
        if not url.endswith("/"):
            url += "/"

        url = settings.REDDIT_ABOUT.format(url)
        response_json = self._send_request(url)
        return self._save_reddit(response_json['data'])

    def import_all_reddits(self):
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
