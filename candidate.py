# -*- coding: utf-8 -*-

# standard libs
from enum import Enum

# project libs
from retry import RetryOnFailure


class SortingStrategy(Enum):

    VIEWS_PER_SECOND = "VIEWS_PER_SECOND"
    BOOKMARKS_PER_SECOND = "BOOKMARKS_PER_SECOND"
    BOOKMARKS_PER_VIEW = "BOOKMARKS_PER_VIEW"

    def __str__(self):
        return self.value


class Candidate(object):

    # how to prioritize candidates
    strategy = SortingStrategy.BOOKMARKS_PER_VIEW

    def __init__(self, id, title, imgurl, views, bookmarks, timedelta):
        self.id = id
        self.title = title
        self.imgurl = imgurl
        self.views = views
        self.bookmarks = bookmarks
        self.timedelta = timedelta

    def __lt_vps(self, other):
        return (self.views / self.timedelta.seconds) > (other.views / other.timedelta.seconds)

    def __lt_bps(self, other):
        return (self.bookmarks / self.timedelta.seconds) > (other.bookmarks / other.timedelta.seconds)

    def __lt_bpv(self, other):
        return (self.bookmarks / self.views) > (other.bookmarks / other.views)

    def __lt__(self, other):
        if not self.valid():
            return False
        if not other.valid():
            return True
        dispatch = {
            SortingStrategy.VIEWS_PER_SECOND: self.__lt_vps,
            SortingStrategy.BOOKMARKS_PER_SECOND: self.__lt_bps,
            SortingStrategy.BOOKMARKS_PER_VIEW: self.__lt_bpv
        }
        return dispatch[Candidate.strategy](other)

    def valid(self):
        return (self.timedelta.seconds > 0) and (self.views > 0)

    def imgpath(self):
        return ("./Images/%s.jpg" % self.id)

    @RetryOnFailure()
    def download(self, api):
        api.download(self.imgurl, path = "./Images", fname = ("%s.jpg" % self.id))

