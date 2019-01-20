
# coding: utf-8

# In[1]:


#import pandas as pd
import requests as rq
from lxml import html
#import numpy as np
from functools import reduce
#from selenium import webdriver
import re
#import pickle
import youtube_dl
from datetime import datetime
import csv


# In[3]:


PLAYLIST_ID = "UUr5zglOqHZAEfCcAx_nw1dQ"


# In[4]:


def call_ytd(playlist_id):

    with youtube_dl.YoutubeDL({'ignoreerrors': True, 'playlistend': 14}) as ydl:
    # with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:

        playd = ydl.extract_info(playlist_id, download=False)

        #with open('playlist.pickle', 'wb') as f:
        #    pickle.dump(playd, f, pickle.HIGHEST_PROTOCOL)

        vids = [vid for vid in playd['entries'] if 1 == 1]
    return vids
    # print(sum('Trump' in vid['title'] for vid in vids), '/', 3)


# In[4]:


#browser = webdriver.Firefox()


# In[5]:


# urls, vids = call_ytd(PLAYLIST_ID)


# In[6]:


# vids[0]


# In[7]:


'''zb = 'Mach mit ihr Schluss!!! 💔- DRUCK -\xa0Folge 13'
zz = 'Die schönste Frau der Welt\xa0💋-\xa0DRUCK - Folge 14'
'Wie lang stehst du schon da? 🥤- DRUCK - 65'
'''


# In[8]:


stat = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[3]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/yt-formatted-string/a"
url = "https://www.youtube.com/watch?v=YiO-wflbYII"


# In[9]:


HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# In[10]:


stats = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[3]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/yt-formatted-string/a"


# In[11]:


def get_site_text(url):
    r = rq.get(url, headers=HEADER)
    return r.text


# In[12]:


def get_yt_text(yt):
    url = str("https://www.youtube.com/watch?v=" + yt)
    return get_site_text(url)


# In[13]:


def get_site(url):
    r = rq.get(url, headers=HEADER)
    text = r.text
    #url_string = bytes(r.text, 'iso-8859-1').decode('utf-8')
    tree = html.document_fromstring(r.text)
    return tree, text


# In[14]:


def filter_trend(txt):
    match = re.search(r"#[\w ]*auf Trends", txt)
    try:
        result = match[0]
    except TypeError:
        result = "#0 auf Trends"
    return result


# In[15]:


def get_trend(yt):
    txt = get_yt_text(yt)
    result = filter_trend(txt)
    return result


# In[16]:


def get_rank(url):
    t = get_trend(url)
    return parse_trend(t)


# In[17]:


def parse_trend(trend):
    tmp = trend.split(" ")
    rank = int(tmp[0][1:]) or 0
    return rank


# In[18]:


def get_yt_info(v):
    yid = v['id']
    s = v['title']
    meta =  extract_title_data(s)
    return meta['vid'], yid, meta


# In[19]:


def match_title(s):
    al = s.split(" ")
    try:
        number = al[-1]
        tmp = "Clip" if al[-2] == '' else "Folge"
    except IndexError:
        return "Z1", "error"            
    return str(tmp[0] + number), tmp


# In[20]:


alist = ""
ai = "Wie lang stehst du schon da? 🥤- DRUCK - 65"


# In[21]:


al = ["DRUCK - Folge 10 - Partyhelden 🚀", "DRUCK - Folge 9 - Abstürze ☠️", "DRUCK - Folge 8 - Blutige Drohung ❗", "DRUCK - Folge 7 - Einmal Schlampe, immer Schlampe!"]


# In[22]:


def extract_title_data(tt):
    try:
        tf = tt.replace("DRUCK - ", "")
        title, tmp = tf.rsplit("-", 1)
    except ValueError:
        return {'title': "Druck der Teaser", 'vid': "Z0", 'kind': "else"}
    try:
        b = int(title.rsplit(" ")[1])
        tmp, title = title, tmp
        aid = tmp.split(" ")[1]
        return {'title': title, 'vid': str('F' + aid), 'kind': "Folge"}
    except:
        pass
    # match = re.search(r"#[\w ]*auf Trends", )
    number, kind = match_title(tmp)
    return {'title': title, 'vid': number, 'kind': kind}


# In[23]:


def get_social_data(yt):
    return yt['view_count'], yt['like_count'], yt['dislike_count']


# In[24]:


def get_trends(yt_list):
    trending = []
    druck_info = []
    for yt in yt_list:
        try:
            vid, yid, meta = get_yt_info(yt)
        except:
            continue
        views, likes, dislikes = get_social_data(yt)
        rank = get_rank(yid)
        meta['yid'] = yid
        time = datetime.utcnow() # TODO fix if fails
        trending.append({'vid': vid, 'rank': rank, 'views': views, 'likes': likes, 'dislikes': dislikes, 'time': time})
        druck_info.append(meta)
    return trending, druck_info


# In[25]:


# trending, d_info = get_trends(vids)


# In[26]:


def trending_to_csv_data(dict_list):
    dataset = []
    for ad in dict_list:
        dataset.append(list(ad.values()))
    return dataset


# In[27]:


def write_data(trending, d_info):
    write_trends(trending, "trending.csv")
    if is_new(d_info):
        write_trends(d_info, "druck.csv")


# In[28]:


def is_new(d_info):
    with open("ids", "r+") as f:
        l = f.readlines()
        did = l[-1]
        did2 = d_info[0]['vid']
        if did2 == did:
            return False
        else:
            f.writelines(did2)
            return True


# In[29]:


#is_new(d_info)


# In[30]:


# d_info


# In[31]:


def write_trends(trending, name):
    keys = trending[0].keys()
    with open(name, 'a+') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writerows(trending)
    return


# In[32]:


def do_druck():
    vids = call_ytd(PLAYLIST_ID)
    trending, d_info = get_trends(vids)
    write_data(trending, d_info)
    return 


# In[33]:


vids = call_ytd(PLAYLIST_ID)


# In[34]:


# vids[80]


# In[35]:


trending, d_info = get_trends(vids)


# In[36]:


write_data(trending, d_info)


# In[37]:


#do_druck()


# In[38]:


# write_data(trending, d_info)


# In[39]:


# trending


# In[40]:


zb = 'Mach mit ihr Schluss!!! 💔- DRUCK -\xa0Folge 13'
zb = 'Die schönste Frau der Welt\xa0💋-\xa0DRUCK - Folge 14'
zc = 'Wie lang stehst du schon da? 🥤- DRUCK - 65'


# In[41]:


# extract_title_data(zc)


# In[42]:


# titlelist, if not in there:
# append & add 
# match Folge 
# else match Druck


# In[43]:


#txt = get_site_text()
txt = '"n"><span class="tv-queue-list-icon yt-sprite"></span></div><h3 class="watch-queue-title">Wiedergabeliste</h3><h3 class="tv-queue-title">Wiedergabeliste</h3><span class="tv-queue-details"></span></div><div class="watch-queue-control-bar control-bar-button"><div class="watch-queue-mole-info"><div class="watch-queue-control-bar-icon"><span class="watch-queue-icon yt-sprite"></span></div><div class="watch-queue-title-container"><span class="watch-queue-count"></span><span class="watch-queue-title">Wiedergabeliste</span><span class="tv-queue-title">Wiedergabeliste</span></div></div>  <span class="dark-overflow-action-menu">\n    \n    \n    <button aria-label="Aktionen für die Wiedergabeliste" class="flip control-bar-button yt-uix-button yt-uix-button-dark-overflow-action-menu yt-uix-button-size-default yt-uix-button-has-icon no-icon-markup yt-uix-button-empty" type="button" aria-expanded="false" aria-haspopup="true" onclick=";return false;" ><span class="yt-uix-button-arrow yt-sprite"></span><ul class="watch-queue-menu yt-uix-button-menu yt-uix-button-menu-dark-overflow-action-menu hid" role="menu" aria-haspopup="true"><li role="menuitem"><span onclick=";return false;" data-action="remove-all" class="watch-queue-menu-choice overflow-menu-choice yt-uix-button-menu-item" >Alle entfernen</span></li><li role="menuitem"><span onclick=";return false;" data-action="disconnect" class="watch-queue-menu-choice overflow-menu-choice yt-uix-button-menu-item" >Beenden</span></li></ul></button>\n  </span>\n  <div class="watch-queue-controls">\n    <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button prev-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Vorheriges Video"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-prev yt-sprite"></span></span></button>\n\n    <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button play-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Wiedergeben"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-play yt-sprite"></span></span></button>\n\n    <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button pause-watch-queue-button yt-uix-button-opacity yt-uix-tooltip hid yt-uix-tooltip" type="button" onclick=";return false;" title="Pausieren"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-pause yt-sprite"></span></span></button>\n\n    <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button next-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Nächstes Video"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-next yt-sprite"></span></span></button>\n  </div>\n</div><div class="autoplay-dismiss-bar fade-out"><span class="autoplay-dismiss-title-label">Das nächste Video wird gestartet</span><span><button class="yt-uix-button yt-uix-button-size-default autoplay-dismiss-button yt-uix-tooltip" type="button" onclick=";return false;" title="Anhalten"><span class="yt-uix-button-content">Anhalten</span></button></span></div></div><div class="watch-queue-items-container yt-scrollbar-dark yt-scrollbar"><div class="yt-uix-scroller playlist-videos-list"><ol class="watch-queue-items-list" data-scroll-action="yt.www.watchqueue.loadThumbnails">  <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n</ol><div class="autoplay-control-container yt-uix-scroller-scroll-unit hid">  <div class="autoplay-control-bar">\n    <label class="autoplay-label" for=autoplay-toggle-id></label>\n    <label class="yt-uix-form-input-checkbox-container yt-uix-form-input-container yt-uix-form-input-paper-toggle-container  "><input class="yt-uix-form-input-checkbox" type="checkbox" id="autoplay-toggle-id"/><div class="yt-uix-form-input-paper-toggle-bg yt-uix-form-input-paper-toggle-bar"></div><div class="yt-uix-form-input-paper-toggle-bg yt-uix-form-input-paper-toggle-button"></div></label>\n  </div>\n</div><div class="up-next-item-container hid"></div></div></div></div>  <div class="hid">\n    <div id="watch-queue-title-msg">\nWiedergabeliste\n    </div>\n\n    <div id="tv-queue-title-msg">Wiedergabeliste</div>\n\n    <div id="watch-queue-count-msg">\n__count__/__total__\n    </div>\n\n    <div id="watch-queue-loading-template">\n      <!--\n          <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n\n      -->\n    </div>\n  </div>\n</div></div>\n    <div id="player-playlist" class="  content-alignment    watch-player-playlist  ">\n          \n\n    </div>\n\n  </div>\n\n  <div class="clear"></div>\n</div><div id="content" class="  content-alignment" role="main">      <div id="placeholder-player">\n    <div class="player-api player-width player-height"></div>\n  </div>\n\n  <div id="watch7-container" class="">\n      <div id="player-messages">\n          <div class="yt-dialog hid mealbar-promo-renderer">\n    <div class="yt-dialog-base">\n      <span class="yt-dialog-align"></span>\n      <div class="yt-dialog-fg" role="dialog">\n        <div class="yt-dialog-fg-content">\n            <div class="yt-dialog-header">\n                  <h2 class="yt-dialog-title" role="alert">\n      YouTube Premium\n  </h2>\n\n            </div>\n          <div class="yt-dialog-loading">\n              <div class="yt-dialog-waiting-content">\n      <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n\n  </div>\n\n          </div>\n          <div class="yt-dialog-content">\n                <div class="mealbar-promo-message" tabindex="0">YouTube ganz ohne Werbeanzeigen genießen.</div>\n\n          </div>\n          <div class="yt-dialog-working">\n              <div class="yt-dialog-working-overlay"></div>\n  <div class="yt-dialog-working-bubble">\n    <div class="yt-dialog-waiting-content">\n        <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\n        Wird verarbeitet...\n    </span>\n  </p>\n\n      </div>\n  </div>\n\n          </div>\n<div class="yt-dialog-footer">      <span class="generic-promo-impression-logging">\n        <span data-feedback-token="AB9zfpIIHBekE6VG_P5cZNEKJ4AsbY12P34-uordmrLHlaxpFGUqeK9Q4JAJ6_jGmkqbepw8HLqo1Gb6x3mbLWo9ziKI4IvJGFEWjG0_BugGEghQn8_6SsDmTsrLyrnlIpVAA9_BgYqPeSO2GM1tqS4jCH7FE7w0TA" class="generic-promo-impression-feedback"></span>\n    </span>\n\n\n\n\n\n\n\n\n\n\n\n\n\n            <div class="service-endpoint-action-container hid">\n    </div>\n\n\n      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-blue-text  vve-check yt-uix-servicelink dismiss-menu-choice" type="button" onclick=";return false;" data-action="hide" data-feedback-token="AB9zfpJPMVsppXHQBZU_zEnFoqMyn_bLKh3pNUjDYt90MdD8HaOVhTzQN4t6qw-MyMhmsncM8IGHVL2qSA7uZbYeJFX7UIUDV8MtbXc45YJlG6ufmb6yt5O1-bOfmMf7karsYxMoJYfVYTrR5ArAJ53oUWN0LyKlDA" data-servicelink="CAUQ7W8iEwidyIjKtenfAhWUYOAKHYguD5Io-B0" data-visibility-tracking="CAUQ7W8iEwidyIjKtenfAhWUYOAKHYguD5Io-B0"><span class="yt-uix-button-content">Nein danke</span></button>\n\n\n\n\n\n\n\n\n\n\n\n\n      <a  href="/premium?ybp=Eg9GRXdoYXRfdG9fd2F0Y2g%253D" class="yt-uix-button   vve-check yt-uix-sessionlink yt-uix-button-primary yt-uix-button-size-default" data-sessionlink="itct=CAYQ7G8iEwidyIjKtenfAhWUYOAKHYguD5Io-B0" data-visibility-tracking="CAYQ7G8iEwidyIjKtenfAhWUYOAKHYguD5Io-B0"><span class="yt-uix-button-content">1 Monat gratis</span></a>\n</div>        </div>\n        <div class="yt-dialog-focus-trap" tabindex="0"></div>\n      </div>\n    </div>\n  </div>\n<div class="mealbar-visibility" data-trigger-condition="TRIGGER_CONDITION_POST_AD" data-lact-th="" data-prompt-del-sec="" data-visibility-tracking="CAQQ42kYASITCJ3IiMq16d8CFZRg4AodiC4Pkij4HQ=="></div>\n  </div>\n  <div id="watch7-main-container">\n    <div id="watch7-main" class="clearfix">\n      <div id="watch7-preview" class="player-width player-height hid">\n      </div>\n      <div id="watch7-content" class="watch-main-col " itemscope itemid="" itemtype="http://schema.org/VideoObject"\n      >\n              <link itemprop="url" href="https://www.youtube.com/watch?v=YiO-wflbYII">\n    <meta itemprop="name" content="Die schönste Frau der Welt 💋- DRUCK - Folge 14">\n    <meta itemprop="description" content="Mehr DRUCK auf Instagram &amp; WhatsApp: Werde Teil unseres WhatsApp Gruppenchats: http://go.funk.net/whatsapp-druck und folge Mia, Hanna, Kiki, Amira, Sam, Jona...">\n    <meta itemprop="paid" content="False">\n\n      <meta itemprop="channelId" content="UCr5zglOqHZAEfCcAx_nw1dQ">\n      <meta itemprop="videoId" content="YiO-wflbYII">\n\n      <meta itemprop="duration" content="PT33M15S">\n      <meta itemprop="unlisted" content="False">\n\n        <span itemprop="author" itemscope itemtype="http://schema.org/Person">\n          <link itemprop="url" href="http://www.youtube.com/channel/UCr5zglOqHZAEfCcAx_nw1dQ">\n        </span>\n        <span itemprop="author" itemscope itemtype="http://schema.org/Person">\n          <link itemprop="url" href="https://plus.google.com/111455831287349369223">\n        </span>\n\n        <script type="application/ld+json" >\n  {\n    "@context": "http://schema.org",\n    "@type": "BreadcrumbList",\n    "itemListElement": [\n      {\n        "@type": "ListItem",\n        "position": 1,\n        "item": {\n          "@id": "http:\\/\\/www.youtube.com\\/channel\\/UCr5zglOqHZAEfCcAx_nw1dQ",\n          "name": "DRUCK - Die Serie"\n        }\n      }\n    ]\n  }\n  </script>\n\n\n    <link itemprop="thumbnailUrl" href="https://i.ytimg.com/vi/YiO-wflbYII/maxresdefault.jpg">\n    <span itemprop="thumbnail" itemscope itemtype="http://schema.org/ImageObject">\n      <link itemprop="url" href="https://i.ytimg.com/vi/YiO-wflbYII/maxresdefault.jpg">\n      <meta itemprop="width" content="1280">\n      <meta itemprop="height" content="720">\n    </span>\n\n\n      <meta itemprop="isFamilyFriendly" content="True">\n      <meta itemprop="regionsAllowed" content="DE">\n      <meta itemprop="interactionCount" content="380990">\n      <meta itemprop="datePublished" content="2019-01-11">\n      <meta itemprop="genre" content="Film &amp; Animation">\n\n      <span itemprop="publication" itemscope itemtype="http://schema.org/BroadcastEvent">\n        <meta itemprop="isLiveBroadcast" content="True">\n            <meta itemprop="startDate" content="2019-01-11T18:14:11+00:00">\n            <meta itemprop="endDate" content="2019-01-11T18:49:26+00:00">\n      </span>\n\n          \n        <div id="watch-header" class="yt-card yt-card-has-padding">\n      <div id="watch7-headline" class="clearfix">\n        <span class="standalone-collection-badge-renderer-text"><a href="/feed/trending" class=" yt-uix-sessionlink      spf-link " data-sessionlink="ei=IHs6XJ24FJTBgQeI3byQCQ" >#9 auf Trends</a></span>\n\n    <div id="watch-headline-title">\n      <h1 class="watch-title-container" >\n        \n\n\n  <span id="eow-title" class="watch-title" dir="ltr" title="Die schönste Frau der Welt\xa0💋-\xa0DRUCK - Folge 14">\n    Die schönste Frau der Welt\xa0💋-\xa0DRUCK - Folge 14\n  </span>\n\n      </h1>\n    </div>\n  </div>\n\n    <div id="watch7-user-header" class=" spf-link ">  <a href="/channel/UCr5zglOqHZAEfCcAx_nw1dQ" class="yt-user-photo yt-uix-sessionlink      spf-link " data-sessionlink="itct=CDsQ4TkiEwidyIjKtenfAhWUYOAKHYguD5Io-B0" >\n      <span class="video-thumb  yt-thumb yt-thumb-48"\n    >\n    <span class="yt-thumb-square">\n      <span class="yt-thumb-clip">\n        \n  <img data-thumb="https://yt3.ggpht.com/a-/AAuE7mAVawg8dIdKnrFgYT7vuCWkhvr3duWky2bi9w=s48-c-k-c0xffffffff-no-rj-mo" height="48" src="/yts/img/pixel-vfl3z5WfW.gif" data-ytimg="1" width="48" alt="DRUCK - Die Serie" onload=";window.__ytRIL &amp;&amp; __ytRIL(this)" >\n\n        <span class="vertical-align"></span>\n      </span>\n    </span>\n  </span>\n\n  </a>\n  <div class="yt-user-info">\n    <a href="/channel/UCr5zglOqHZAEfCcAx_nw1dQ" class="yt-uix-sessionlink       spf-link " data-sessionlink="itct=CDsQ4TkiEwidyIjKtenfAhWUYOAKHYguD5Io-B0" >DRUCK - Die Serie</a>\n  </div>\n<span id="watch7-subscription-container"><span class=" yt-uix-button-subscription-container"><span class="unsubscribe-confirmation-overlay-container">  \n  <div class="yt-uix-overlay "  data-overlay-style="primary" data-overlay-shape="tiny">\n    \n        <div class="yt-dialog hid ">\n    <div class="yt-dialog-base">\n      <span class="yt-dialog-align"></span>\n      <div class="yt-dialog-fg" role="dialog">\n        <div class="yt-dialog-fg-content">\n          <div class="yt-dialog-loading">\n              <div class="yt-dialog-waiting-content">\n      <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n\n  </div>\n\n          </div>\n          <div class="yt-dialog-content">\n              <div class="unsubscribe-confirmation-overlay-content-container">\n    <div class="unsubscribe-confirmation-overlay-content">\n      <div class="unsubscribe-confirmation-message">\n        Abo für DRUCK - Die Serie beenden?\n      </div>\n    </div>\n\n    <div class="yt-uix-overlay-actions">\n      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-default yt-uix-overlay-close" type="button" onclick=";return false;"><span class="yt-uix-button-content">Abbrechen</span></button>\n      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-primary overlay-confirmation-unsubscribe-button yt-uix-overlay-close" type="button" onclick=";return false;"><span class="yt-uix-button-content">Abo beenden</span></button>\n    </div>\n  </div>\n\n          </div>\n          <div class="yt-dialog-working">\n              <div class="yt-dialog-working-overlay"></div>\n  <div class="yt-dialog-working-bubble">\n    <div class="yt-dialog-waiting-content">\n        <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\n        Wird verarbeitet...\n    </span>\n  </p>\n\n      </div>\n  </div>\n\n          </div>\n        </div>\n        <div class="yt-dialog-focus-trap" tabindex="0"></div>\n      </div>\n    </div>\n  </div>\n\n\n  </div>\n\n</span><button class="yt-uix-button yt-uix-button-size-default yt-uix-button-subscribe-branded yt-uix-button-has-icon no-icon-markup yt-uix-subscription-button yt-can-buffer yt-uix-servicelink vve-check" type="button" onclick=";return false;" aria-live="polite" aria-busy="false" data-href="https://accounts.google.com/ServiceLogin?service=youtube&amp;uilel=3&amp;continue=http%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26feature%3Dsubscribe%26action_handle_signin%3Dtrue%26hl%3Dde%26continue_action%3DQUFFLUhqbGwzWUVQakRLUVZ0S2R1bTlzY2ZQX2VtcjdVUXxBQ3Jtc0ttMzYyeEtSai1RR0tBQUhqM1ZTZFJxczV1VHR0TmEyUkc4WTVkRUZLV2V3a3VCcUY3eV9VTTF1TjcwLWxlQXVKZnhhc2dITlZZZjZWekNlU1kyam0tODBNOEdfbnIzMWJGaVowNGNqTDNiem4tWHhOU3R0VUxBRjJ0bmlBdHJZN01IQWFRZkpsM2RaZXNWRFN6d085cGp0MlFLdzhJT3FWZjluVG1qVFk0UC0tT1llOGRyZEFjS3NZeGM2WkFweENCN254RFk%253D%26next%3D%252Fchannel%252FUCr5zglOqHZAEfCcAx_nw1dQ&amp;hl=de&amp;passive=true" data-channel-external-id="UCr5zglOqHZAEfCcAx_nw1dQ" data-show-unsub-confirm-dialog="true" data-clicktracking="itct=CDwQmysiEwidyIjKtenfAhWUYOAKHYguD5Io-B0yBXdhdGNo" data-servicelink="CDwQmysiEwidyIjKtenfAhWUYOAKHYguD5Io-B0yBXdhdGNo" data-visibility-tracking="CDwQmysiEwidyIjKtenfAhWUYOAKHYguD5Io-B0yBXdhdGNo" data-show-unsub-confirm-time-frame="always" data-style-type="branded" data-subscribed-timestamp="0"><span class="yt-uix-button-content"><span class="subscribe-label" aria-label="Abonnieren">Abonnieren</span><span class="subscribed-label" aria-label="Abo beenden">Abonniert</span><span class="unsubscribe-label" aria-label="Abo beenden">Abo beenden</span></span></button><button class="yt-uix-button yt-uix-button-size-default yt-uix-button-default yt-uix-button-empty yt-uix-button-has-icon yt-uix-subscription-preferences-button" type="button" onclick=";return false;" aria-label="Abo-Einstellungen" aria-live="polite" aria-role="button" aria-busy="false" data-channel-external-id="UCr5zglOqHZAEfCcAx_nw1dQ"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-subscription-preferences yt-sprite"></span></span></button><span class="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count" title="187.983" aria-label="187.983" tabindex="0">187.983</span>  <span class="subscription-preferences-overlay-container">\n    \n  <div class="yt-uix-overlay "  data-overlay-style="primary" data-overlay-shape="tiny">\n    \n        <div class="yt-dialog hid ">\n    <div class="yt-dialog-base">\n      <span class="yt-dialog-align"></span>\n      <div class="yt-dialog-fg" role="dialog">\n        <div class="yt-dialog-fg-content">\n          <div class="yt-dialog-loading">\n              <div class="yt-dialog-waiting-content">\n      <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n\n  </div>\n\n          </div>\n          <div class="yt-dialog-content">\n              <div class="subscription-preferences-overlay-content-container">\n    <div class="subscription-preferences-overlay-loading ">\n        <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\nWird geladen...\n    </span>\n  </p>\n\n    </div>\n    <div class="subscription-preferences-overlay-content">\n    </div>\n  </div>\n\n          </div>\n          <div class="yt-dialog-working">\n              <div class="yt-dialog-working-overlay"></div>\n  <div class="yt-dialog-working-bubble">\n    <div class="yt-dialog-waiting-content">\n        <p class="yt-spinner ">\n        <span title="Ladesymbol" class="yt-spinner-img  yt-sprite"></span>\n\n    <span class="yt-spinner-message">\n        Wird verarbeitet...\n    </span>\n  </p>\n\n      </div>\n  </div>\n\n          </div>\n        </div>\n        <div class="yt-dialog-focus-trap" tabindex="0"></div>\n      </div>\n    </div>\n  </div>\n\n\n  </div>\n\n  </span>\n</span></span></div>\n    <div id="watch8-action-buttons" class="watch-action-buttons clearfix"><div id="watch8-secondary-actions" class="watch-secondary-actions yt-uix-button-group" data-button-toggle-group="optional">    <span class="yt-uix-clickcard">\n      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup yt-uix-clickcard-target addto-button pause-resume-autoplay yt-uix-tooltip" type="button" onclick=";return false;" title="Hinzufügen" data-orientation="vertical" data-position="bottomleft"><span class="yt-uix-button-content">Hinzufügen</span></button>\n        <div class="signin-clickcard yt-uix-clickcard-content">\n    <h3 class="signin-clickcard-header">Möchtest du dieses Video später noch einmal ansehen?</h3>\n    <div class="signin-clickcard-message">\n      Wenn du bei YouTube angemeldet bist, kannst du dieses Video zu einer Playlist hinzufügen.\n    </div>\n    <a  href="https://accounts.google.com/ServiceLogin?service=youtube&amp;uilel=3&amp;continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26hl%3Dde%26feature%3D__FEATURE__%26action_handle_signin%3Dtrue%26next%3D%252Fwatch%253Fv%253DYiO-wflbYII&amp;hl=de&amp;passive=true" class="yt-uix-button  signin-button yt-uix-sessionlink yt-uix-button-primary yt-uix-button-size-default" data-sessionlink="ei=IHs6XJ24FJTBgQeI3byQCQ"><span class="yt-uix-button-content">Anmelden</span></a>\n  </div>\n\n    </span>\n  <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup pause-resume-autoplay action-panel-trigger action-panel-trigger-share   yt-uix-tooltip" type="button" onclick=";return false;" title="Teilen\n" data-trigger-for="action-panel-share" data-button-toggle="true"><span class="yt-uix-button-content">Teilen\n</span></button>\n<div class="yt-uix-menu " >  <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup pause-resume-autoplay yt-uix-menu-trigger yt-uix-tooltip" type="button" onclick=";return false;" title="Mehr Aktionen" aria-pressed="false" aria-label="Action menu." aria-haspopup="true" role="button" id="action-panel-overflow-button"><span class="yt-uix-button-content">Mehr</span></button>\n<div class="yt-uix-menu-content yt-ui-menu-content yt-uix-menu-content-hidden" role="menu"><ul id="action-panel-overflow-menu">  <li>\n      <span class="yt-uix-clickcard" data-card-class=report-card>\n          <button type="button" class="yt-ui-menu-item has-icon action-panel-trigger action-panel-trigger-report report-button yt-uix-clickcard-target"\n data-orientation="horizontal" data-position="topright">\n    <span class="yt-ui-menu-item-label">Melden</span>\n  </button>\n\n          <div class="signin-clickcard yt-uix-clickcard-content">\n    <h3 class="signin-clickcard-header">Möchtest du dieses Video melden?</h3>\n    <div class="signin-clickcard-message">\n "'


# In[44]:


# a = get_trend(txt)#


# In[45]:


# a

