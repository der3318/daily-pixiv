
## 📰 Daily Pixiv Notification

![pixivpy3](https://img.shields.io/badge/pixivpy3%20%28pip3%29-3.7.2-blue.svg)
![line](https://img.shields.io/badge/line-notify--api.line.me-brightgreen.svg)
![rich](https://img.shields.io/badge/rich%20%28pip3%29-13.3.1-pink.svg)
![pillow](https://img.shields.io/badge/pillow%20%28pip3%29-9.4.0-yellow.svg)
![license](https://img.shields.io/badge/license-MIT%20%28inherited%29-blueviolet.svg)

The repo leverages [pixivpy (Pixiv API)](https://github.com/upbit/pixivpy) and free [Github Actions](../../actions) to download top ranked Pixiv illustrations into a [Line chatroom (via Line Notify)](https://notify-bot.line.me/my/) on a daily basis.

![Sample.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/Sample.png)


### Activate Github Workflow Pipeline

[schedule.yml](https://github.com/der3318/daily-pixiv/blob/main/.github/workflows/schedule.yml) has several predefined configurations. For Pixiv token, keyword (tag) and Line Notify bearer, they should be provided as [Github Action secrets](../../settings/secrets/actions):

![ActionSecrets.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/ActionSecrets.png)

| Secret Name | Description |
| :- | :- |
| LINE_BEARER | the bearer used by Line Notify to interact with a chatroom (a str including alphabets and numbers) |
| PIXIV_KEYWORD | the tag keyword to search (likely to be a Japanese term) |
| PIXIV_TOKEN | a Pixiv refresh session token (usually a 43-charactered str including alphabets and numbers) |

By default, the workflow is scheduled at 5AM (UTC+0) every day. It surfs the artworks and pushs a notification on succeeded.


### How to Get Pivix Refresh Token

See [@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) for detailed instructions and scripts.

TL;DR

* Run `python3 pixiv_auth.py login` and the browser will open a Pixiv auth page asking for sign-in. Stay and do not proceed at the moment.
* Open dev console (F12) and switch to network view. Enter `callback?state` in the filter box.
* Now continue to proceed with Pixiv Login. A request will be captured. Copy its `code` parameter. (@AlttiRi's example)

    ![Capture.png](https://user-images.githubusercontent.com/16310547/145266319-61513da9-038d-4cef-bcbf-9435742d4ba9.png)

* Go back to the python cmd prompt. Paste the code and hit the enter key.
* `access_token`, `refresh_token` and `expires_in` will be displyed. `refresh_token` is exactly what we need.

It seems that `refresh_token` can be used for a very long period (months and even years). Do this once, keep the token as secrets and make it accessible for pipeline.


### Local Run

To debug or add new features, the tool can be run locally. It saves downloaded images to `Images/` directly, using original resolution (unlike Line Notify which has a size limitation).

![LocalRun.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/LocalRun.png)


### Known (and Mitigated) Issue

```shell
cloudscraper.exceptions.CloudflareChallengeError: Detected a Cloudflare version 2 Captcha challenge, This feature is not available in the opensource (free) version.

During handling of the above exception, another exception occurred:

pixivpy3.utils.PixivError: requests POST https://oauth.secure.pixiv.net/auth/token error: Detected a Cloudflare version 2 Captcha challenge, This feature is not available in the opensource (free) version.
```

According to https://github.com/upbit/pixivpy/issues/166, retry is the most trivial solution. That's why the script has a [RetryOnFailure](https://github.com/der3318/daily-pixiv/blob/main/retry.py) module.
