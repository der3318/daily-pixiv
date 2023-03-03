# -*- coding: utf-8 -*-

# standard libs
from argparse import ArgumentParser
from datetime import datetime, timezone

# third party libs
from pixivpy3 import AppPixivAPI    # pip install pixivpy3
from rich import inspect            # pip install rich

# project libs
from candidate import Candidate, SortingStrategy
from line import LineNotifyClient
from retry import RetryOnFailure


@RetryOnFailure()
def init(token, keyword):
    api = AppPixivAPI()
    api.auth(refresh_token = token)
    results = api.search_illust(keyword, search_target = "partial_match_for_tags", duration = "within_last_day")
    return api, results


def main():

    # arg parser
    parser = ArgumentParser()
    
    # required parameters
    parser.add_argument("--token", type = str, required = True, help = "pixiv refresh token")
    parser.add_argument("--keyword", type = str, required = True, help = "keyword to search")
    
    # optional parameters
    parser.add_argument("--strategy", type = SortingStrategy, default = Candidate.strategy, choices = list(SortingStrategy))
    parser.add_argument("--count", type = int, default = 3, help = "max illusts to save")
    parser.add_argument("--roft", type = int, default = RetryOnFailure.trials, help = "max iterations to try on failure")
    parser.add_argument("--rofc", type = int, default = RetryOnFailure.cooldown, help = "interval in seconds for trials on failure")
    parser.add_argument("--linebearer", type = str, help = "line notify bearer")
    
    # parse and set static config
    args = parser.parse_args()
    RetryOnFailure.trials = args.roft
    RetryOnFailure.cooldown = args.rofc
    Candidate.strategy = args.strategy

    # init and get illusts
    api, results = init(args.token, args.keyword)

    # collect daily candidates
    candidates = list()
    for idx, illust in enumerate(results.illusts):
        image = illust.meta_single_page.get("original_image_url", illust.image_urls.large)
        delta = datetime.now(timezone.utc) - datetime.strptime(illust.create_date, "%Y-%m-%dT%H:%M:%S%z")
        if delta.total_seconds() < 86400:
            candidates.append(Candidate(illust.id, illust.title, image, illust.total_view, illust.total_bookmarks, delta))

    # save top ranked images and notify
    for idx, candidate in enumerate(sorted(candidates)[:args.count]):
        inspect(candidate)
        candidate.download(api)
        if args.linebearer:
            message = ("%s\n(%d views, %d bookmarks)" % (candidate.title, candidate.views, candidate.bookmarks))
            LineNotifyClient(args.linebearer).send(message, candidate.imgpath())


if __name__ == "__main__":
    main()

