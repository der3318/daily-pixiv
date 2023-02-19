# -*- coding: utf-8 -*-

# standard libs
from os import path, stat
from requests import post

# third party libs
from PIL import Image   # pip install pillow

# project libs
from retry import RetryOnFailure


class LineNotifyClient(object):

    # line notify endpoint
    endpoint = "https://notify-api.line.me/api/notify"

    # HTTP request limit (2.5MiB)
    sizelimit = 2621440

    # thumbnail size (keep ratio)
    thumbsize = 512, 512

    def __init__(self, bearer):
        self.bearer = bearer

    def __thumbnail(self, imgpath):
        thumbnailpath = path.splitext(imgpath)[0] + ".thumbnail.jpg"
        with Image.open(imgpath) as im:
            rgb = im.convert("RGB")
            rgb.thumbnail(LineNotifyClient.thumbsize)
            rgb.save(thumbnailpath)
        return thumbnailpath

    @RetryOnFailure()
    def send(self, message, imgpath):
        headers = {"Authorization": ("Bearer %s" % self.bearer)}
        data = {"message": message}
        if stat(imgpath).st_size >= LineNotifyClient.sizelimit:
            imgpath = self.__thumbnail(imgpath)
        with open(imgpath, "rb") as img:
            files = {"imageFile": img}
            res = post(LineNotifyClient.endpoint, headers = headers, data = data, files = files)
            res.raise_for_status()

