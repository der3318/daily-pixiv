
## 📰 Daily Pixiv Notification

![pixivpy3](https://img.shields.io/badge/pixivpy3%20%28pip3%29-3.7.2-blue.svg)
![line](https://img.shields.io/badge/line-api.line.me%2Fv2%2Fbot%2Fmessage%2Fpush-brightgreen.svg)
![rich](https://img.shields.io/badge/rich%20%28pip3%29-13.3.1-pink.svg)
![pillow](https://img.shields.io/badge/pillow%20%28pip3%29-9.4.0-yellow.svg)
![license](https://img.shields.io/badge/license-MIT%20%28inherited%29-blueviolet.svg)

The repo leverages [pixivpy (Pixiv API)](https://github.com/upbit/pixivpy) to download top ranked Pixiv illustrations into a [LINE chatroom (via LINE Notify)](https://notify-bot.line.me/my/). A [Github Actions](../../actions) job is also setup to test the flow and verify the integration (incl. API, endpoints, large payload requests) on a daily basis.

> [!NOTE]
> [LINE Notify service will be inoperable](https://notify-bot.line.me/closing-announce) in April 2025. The official recommendation is to [use Messaging API as alternative methods of sending notifications](https://techblog.lycorp.co.jp/zh-hant/line-notify-migration-tips).

![Sample.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/Sample.png)


### About Github Workflow Pipeline

[schedule.yml](https://github.com/der3318/daily-pixiv/blob/main/.github/workflows/schedule.yml) has several predefined configurations. For Pixiv token, keyword (tag) and LINE Notify bearer, they are provided as [Github Action secrets](../../settings/secrets/actions):

![ActionSecrets.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/ActionSecrets.png)

| Secret Name | Description |
| :- | :- |
| <del>LINE_BEARER</del> | <del>the bearer used by LINE Notify to interact with a chatroom (a str including alphabets and numbers)</del> |
| LINE_TOKEN | the channel access token of your LINE business ID for authorization |
| LINE_GROUP | group ID of the chatroom (can be found from the webhook event object, for example, using https://webhook.site/) |
| PIXIV_KEYWORD | the tag keyword to search (likely to be a Japanese term) |
| PIXIV_TOKEN | a Pixiv refresh session token (usually a 43-charactered str including alphabets and numbers) |

By default, the workflow is scheduled at 5AM (UTC+0) every day. It surfs the artworks and pushs a notification on success.


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

To customize or add new features, run the scripts locally. It saves downloaded images to `Images/` directly, using original resolution (unlike LINE Notify which has a size limitation).

![LocalRun.png](https://github.com/der3318/daily-pixiv/blob/main/Demo/LocalRun.png)


### Known (and Mitigated) Issue

```shell
cloudscraper.exceptions.CloudflareChallengeError: Detected a Cloudflare version 2 Captcha challenge, This feature is not available in the opensource (free) version.

During handling of the above exception, another exception occurred:

pixivpy3.utils.PixivError: requests POST https://oauth.secure.pixiv.net/auth/token error: Detected a Cloudflare version 2 Captcha challenge, This feature is not available in the opensource (free) version.
```

According to https://github.com/upbit/pixivpy/issues/166, retry is the most trivial solution. That's why the script has a [RetryOnFailure](https://github.com/der3318/daily-pixiv/blob/main/retry.py) module.


### Github Terms and Agreement

See [Acceptable Use Polices Regarding Actions](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#actions):

* This is NOT for commercial purposes.
* Runs are low burden and will NOT deliver content publicly.
* Activities are considered sort of software project testing.

