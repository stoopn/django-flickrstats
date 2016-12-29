import flickrapi
import datetime
import calendar
import os
import sys
import pytz
import time

proj_path = "/Users/norbert/Code/djangosite/"
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangosite.settings")
os.chdir(proj_path)

try:
    import flickrsecret
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from flickrstats.models import FlickrUser, Photo, DayStatistic
    from flickrstats.models import Favorite, PhotoStat, Comment
except:
    print "Unable to import flickrstats model"

flickr = flickrapi.FlickrAPI(flickrsecret.api_key, flickrsecret.api_secret,
                             format='parsed-json')
flickr.authenticate_via_browser(perms='read')

utc = pytz.utc


def add_update_photos(ds=None):
    if ds is None:
        ts = 0
        print "Getting all photos from photostream"
    else:
        ts = ds.ts_range()[1]  # Update photos uploaded after end of last ds
        print "Getting photos uploaded after %s" % ds.date
    page = 1
    pages = 1

    while page <= pages:
        newphotos = flickr.photos.search(
            user_id="me", min_upload_date=ts, page=page, perpage=100)['photos']
        pages = newphotos['pages']
        if pages == 0:
            page += 1
            continue
        print "Getting photos... page %i/%i" % (page, pages)
        for photo in newphotos['photo']:
            pid = int(photo['id'])
            ph = Photo.objects.filter(id=pid).first()
            if ph is None:
                ph = Photo(id=pid)
            ph.title = photo['title']
            info = flickr.photos.getInfo(photo_id=pid)['photo']
            ph.date_posted = utc.localize(datetime.datetime.fromtimestamp(
                int(info['dateuploaded'])))
            ph.date_taken = info['dates']['taken']
            ph.total_views = int(info['views'])
            ph.total_comments = int(info['comments']['_content'])
            ph.save()
            # Get favorites for this photo:
            update_favorites(ph)
            update_comments(ph)
            time.sleep(1)
        page += 1


def add_user(userid, username):
    user = FlickrUser(userid=userid, name=username)
    user.save()
    return user


def update_favorites(photo, ds=None):
    pid = photo.id
    if ds is None:
        Favorite.objects.filter(photo=photo).delete()
        startts = 0
        endts = 0
        print "Downloading all favorites for photo %i" % pid
    else:
        [startts, endts] = ds.ts_range()
        startdate = utc.localize(datetime.datetime.fromtimestamp(startts))
        enddate = utc.localize(datetime.datetime.fromtimestamp(endts))
        Favorite.objects.filter(photo=photo, date__date__gte=startdate,
                                date__date__lt=enddate).delete()
        print "Downloading daily favorites for photo %i" % pid
    page = 1
    pages = 1
    while page <= pages:
        res = flickr.photos.getFavorites(photo_id=pid,
                                         page=page, perpage=50)['photo']
        pages = res['pages']
        if page == 1:
            photo.total_favorites = int(res['total'])
        if pages == 0:
            page += 1
            continue
        favs = res['person']
        for fav in favs:
            favts = int(fav['favedate'])
            if ds is not None and (favts >= endts or favts < startts):
                continue  # Nothing to be done for old or future favorites
            newfav = Favorite(
                photo=photo,
                date=utc.localize(datetime.datetime.fromtimestamp(favts)))
            userid = str(fav['nsid'])
            user = FlickrUser.objects.filter(userid=userid).first()
            if user is None:
                user = add_user(userid, fav['username'])
            newfav.user = user
            newfav.save()
        page += 1
    photo.save()


def update_comments(photo, ds=None):
    pid = photo.id
    if ds is None:
        Comment.objects.filter(photo=photo).delete()
        startts = 0
        endts = 0
        print "Downloading all comments for photo %i" % pid
    else:
        [startts, endts] = ds.ts_range()
        startdate = utc.localize(datetime.datetime.fromtimestamp(startts))
        enddate = utc.localize(datetime.datetime.fromtimestamp(endts))
        Comment.objects.filter(photo=photo, date__date__gte=startdate,
                               date__date__lt=enddate).delete()
        print "Downloading daily comments for photo %i" % pid

    res = flickr.photos.comments.getList(photo_id=pid)['comments']
    if 'comment' in res:
        comments = res['comment']
        photo.total_comments = len(comments)
        for comment in comments:
            commts = int(comment['datecreate'])
            if ds is not None and (commts >= endts or commts < startts):
                continue  # Nothing to do for old or future comments
            newcomment = Comment(
                photo=photo,
                date=utc.localize(datetime.datetime.fromtimestamp(commts)))
            userid = str(comment['author'])
            user = FlickrUser.objects.filter(userid=userid).first()
            if user is None:
                user = add_user(userid, comment['authorname'])
            newcomment.user = user
            newcomment.save()
    else:
        photo.total_comments = 0
        photo.save()


def aggregate_daily_photo_stats(ds):
    page = 1
    pages = 1
    ts = ds.ts
    while page <= pages:
        res = flickr.stats.getPopularPhotos(date=ts, page=page, perpage=100)
        pages = res['photos']['pages']
        if pages == 0:
            page += 1
            continue
        photos = res['photos']['photo']
        print "Aggregating daily stats for %s... page %i/%i" % (ds.date, page, pages)
        for photo in photos:
            pid = int(photo['id'])
            try:  # photo should exist at this point
                ph = Photo.objects.get(id=pid)
            except:
                print "Error: Photo with id=" + str(pid)
                + " does not exist in local DB"
                exit()
            ps = PhotoStat(photo=ph, daystatistic=ds)
            ps.favorites = int(photo['stats']['favorites'])
            ps.views = int(photo['stats']['views'])
            ps.comments = int(photo['stats']['comments'])
            ph.total_views = int(photo['stats']['total_views'])
            ph.total_comments = int(photo['stats']['total_comments'])
            ph.total_favorites = int(photo['stats']['total_favorites'])
            ps.save()
            ph.save()
            if ps.favorites > 0:
                update_favorites(ph, ds)
            if ps.comments > 0:
                update_comments(ph, ds)
            time.sleep(1)
        page += 1


# Get the first of 28 days available:
utc_now = datetime.datetime.utcnow()
utc_today = datetime.date(utc_now.year, utc_now.month, utc_now.day)
yesterday = utc_today - datetime.timedelta(days=1)
earliestday = utc_today - datetime.timedelta(days=28)
earliestts = calendar.timegm(earliestday.timetuple())
yesterdayts = calendar.timegm(yesterday.timetuple())
try:
    laststat = DayStatistic.objects.order_by('-ts')[0]
    print "Last aggregation on %s" % laststat.date
    if laststat.ts >= yesterdayts:
        print "Nothing to be done: All available statistics is aggregated."
        exit()
    print "We have new statistics to aggregate!"
    # First, get all new photos
    add_update_photos(laststat)
    if laststat.ts < earliestts:
        #  We haven't updated for more than 28 days
        #  Create the first available day statistics:
        firstdate = earliestday
    else:
        firstdate = laststat.date + datetime.timedelta(days=1)
except IndexError:
    #  No daily statistics yet => add photos, then get last 28 daily stats:
    add_update_photos()
    firstdate = earliestday
#
#  Main loop: Find out how many days to sync:
#
currdate = firstdate
while currdate <= yesterday:
    currdatets = calendar.timegm(currdate.timetuple())
    currstat = DayStatistic(date=currdate,
                            ts=currdatets)
    currstat.save()
    aggregate_daily_photo_stats(currstat)
    currdate = currdate + datetime.timedelta(days=1)
