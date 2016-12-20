import webapp2
import jinja2
import os
import urllib2
import sys
import logging
from google.appengine.ext import db
from google.appengine.api import memcache
from xml.dom import minidom


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# art_key = db.Key.from_path('ascii_chan', 'arts')

IP_URL = "http://freegeoip.net/%(format)s/%(IP)s"
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"


def get_coords(ip):
    url = IP_URL % {'format': 'xml', 'IP': ip}
    content = None
    try:
        content = urllib2.urlopen(url).read()

    except urllib2.URLError:
        return

    if content:
        d = minidom.parseString(content)
        lat_el = d.getElementsByTagName("Latitude")
        lon_el = d.getElementsByTagName("Longitude")

        if lat_el and lon_el:
            # How crazy is that?? Thank you minidom
            lon, lat = lon_el[0].firstChild.nodeValue, lat_el[0].firstChild.nodeValue
            return db.GeoPt(lat, lon)


def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers


def top_arts(update=False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB_QUERY")
        arts = db.GqlQuery("SELECT * "
                           "FROM Art "
                           "ORDER BY created DESC ")
        arts = list(arts)
        memcache.set(key, arts)
    return arts


def console(s):
    sys.stderr.write('%s\n' % s)


class Handler(webapp2.RequestHandler):
    """Useful functions for jinja2 templates"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
            self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    coords = db.GeoPtProperty()


class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()

        img_url = None
        points = filter(None, (a.coords for a in arts))
        if points:
            img_url = gmaps_img(points)

        self.render('front.html', title=title, art=art, error=error, arts=arts, img_url=img_url)

    def get(self):
        # self.write(repr(get_coords(self.request.remote_addr)))
        self.render_front()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title=title, art=art)
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords
            a.put()
            top_arts(True)
            self.redirect('/')
        else:
            error = "we need both a title and some artwork"
            self.render_front(title=title, art=art, error=error)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
