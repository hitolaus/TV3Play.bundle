VIDEO_PREFIX = "/video/tv3play"

ART = 'art-default.png'
ICON = 'icon-default.png'

BASE_URL_DK = 'http://www.tv3play.dk'
BASE_URL_SE = 'http://www.tv3play.se'
BASE_URL_NO = 'http://www.tv3play.no'

BASE_URL = BASE_URL_DK

API_BASE = '/mobileapi/'

FEATURED_API = API_BASE + 'featured'
MOSTVIEWED_API = API_BASE + 'mostviewed'
ALL_API = API_BASE + 'format'
DETAILED_API = API_BASE + 'detailed?videoid='

IMAGE_URL_SMALL = 'http://play.pdl.viaplay.com/imagecache/290x162/'


####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')
    ObjectContainer.view_group = 'List'

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


# This main function will setup the displayed items.
@handler(VIDEO_PREFIX, L('Title'), ICON, ART)
def MainMenu():

    country = Prefs['site']
    if (country == "SE"):
        BASE_URL = BASE_URL_SE
    elif (country == "NO"):
        BASE_URL = BASE_URL_NO

    oc = ObjectContainer()

    oc.add(DirectoryObject(
        key=Callback(RecommendedList),
        title=L('Recommended Menu Title'),
        summary='',
        thumb=R('icon-bookmark.png')))
    oc.add(DirectoryObject(
        key=Callback(MostViewedList),
        title=L('Most Viewed Menu Title'),
        thumb=R('icon-popular.png')))
    oc.add(DirectoryObject(
        key=Callback(LatestProgramsList),
        title=L('Latest Programs Menu Title'),
        thumb=R('icon-popular.png')))
    #oc.add(DirectoryObject(
    #    key=Callback(AllList),
    #    title=L('All Menu Title'),
    #    thumb=R('icon-menu.png')))
    oc.add(PrefsObject(title=L('Preferences Menu Title'), thumb=R('icon-prefs.png')))

    return oc


def RecommendedList():
    oc = ObjectContainer()
    # recommended / latest_programs / latest_clips
    for item in JSON.ObjectFromURL(BASE_URL + FEATURED_API)['recommended']:
        oc.add(VideoClipObject(
                title=item['title'],
                summary=item['description'],
                thumb=Resource.ContentsOfURLWithFallback(IMAGE_URL_SMALL + item['image'], R('icon-movie.png')),
                url=BASE_URL + DETAILED_API + item['id']))

    return oc


def LatestProgramsList():
    oc = ObjectContainer()
    for item in JSON.ObjectFromURL(BASE_URL + FEATURED_API)['latest_programs']:
        oc.add(VideoClipObject(
                title=item['title'],
                summary=item['description'],
                thumb=Resource.ContentsOfURLWithFallback(IMAGE_URL_SMALL + item['image'], R('icon-movie.png')),
                url=BASE_URL + DETAILED_API + item['id']))

    return oc


def MostViewedList():
    oc = ObjectContainer()
    for item in JSON.ObjectFromURL(BASE_URL + MOSTVIEWED_API)[0]['videos']:
        oc.add(VideoClipObject(
                title=item['title'],
                summary=item['description'],
                thumb=Resource.ContentsOfURLWithFallback(IMAGE_URL_SMALL + item['image'], R('icon-movie.png')),
                url=BASE_URL + DETAILED_API + item['id']))

    return oc


def AllList():
    oc = ObjectContainer()
    return oc
