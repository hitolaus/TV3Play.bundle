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
        thumb=R('icon-flaged.png')))
    #oc.add(DirectoryObject(
    #    key=Callback(AllList),
    #    title=L('All Menu Title'),
    #    thumb=R('icon-menu.png')))
    oc.add(PrefsObject(title=L('Preferences Menu Title'), thumb=R('icon-prefs.png')))

    return oc


def RecommendedList():
    oc = ObjectContainer()
    for item in JSON.ObjectFromURL(BASE_URL + FEATURED_API)['recommended']:
        oc.add(ParseEpisode(item))

    return oc


def LatestProgramsList():
    oc = ObjectContainer()
    for item in JSON.ObjectFromURL(BASE_URL + FEATURED_API)['latest_programs']:
        oc.add(ParseEpisode(item))

    return oc


def MostViewedList():
    oc = ObjectContainer()
    for item in JSON.ObjectFromURL(BASE_URL + MOSTVIEWED_API)[0]['videos']:
        oc.add(ParseEpisode(item))

    return oc


def AllList():
    oc = ObjectContainer()
    return oc


##
# Parses the following
# {
#     id: "295806",
#     type: "video_program",
#     title: "Paradise Hotel 2013 S09E01",
#     summary: "Intet er sikkert, og alt er langt fra, som gæsterne forventer det, når TV3 åbner dørene til Paradise Hotel 2013 og lader sommerfuglen flyve afsted mod den halve million.",
#     description: "Som altid er der farlige alliancer, spirende romancer og kærlighed blandt gæsterne, der kæmper om titlen som årets vinder af Paradise Hotel og den halve million kroner. Hotellet er igen gjort klar, og værelserne Cobra, Cocodrilo, Flamingo, Geco og Leopardo har fået et helt nyt og lækkert look, mens Solo-værelset mest af alt ligner et gammelt nedslidt omklædningsrum. Alle deltagerne er spændt til bristepunktet, og de er mere end klar til at tjekke ind i de flotte og luksuriøse omgivelser på Paradise Hotel 2013. Vejen til finalen er lang, og der er blevet fyret godt op under sombreroen i år, så der er masser af skæve twists og store oplevelser for de uvidende gæster, som tjekker ind på det mondæne mexicanske hotel. ",
#     image: "category_pictures/Rikke2.jpg",
#     length: "2492",
#     expiration: null,
#     created: "1358180317",
#     updated: "1360154093",
#     formatcategoryid: "4789",
#     formatid: "3823",
#     formattitle: "Paradise Hotel",
#     airdate: "2013-01-14 21:00:00",
#     season: "9",
#     episode: "1"
# }
def ParseEpisode(item):
    try:
        duration = int(item['length']) * 1000
    except:
        duration = None

    try:
        season = int(item['season'])
        episode = int(item['episode'])
    except:
        episode = None
        season = None

    try:
        airdate = Datetime.ParseDate(item['airdate']).date()
    except:
        airdate = None

    return EpisodeObject(
        show=item['formattitle'],
        title=item['title'],
        season=season,
        index=episode,
        summary=item['description'],
        duration=duration,
        originally_available_at=airdate,
        thumb=Resource.ContentsOfURLWithFallback(IMAGE_URL_SMALL + item['image'], R('icon-movie.png')),
        url=BASE_URL + DETAILED_API + item['id'])
