# Copyright (C) 2011 Philter Phactory Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X
# CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of Philter Phactory Ltd. shall
# not be used in advertising or otherwise to promote the sale, use or other
# dealings in this Software without prior written authorization from Philter
# Phactory Ltd.

import logging
import random
import re
import simplejson
import time
import urllib


QWIKI_QUERY = "http://embed-api.qwiki.com/api/v1/search.json?count=1&"
QWIKI_FOUND_NOTHING = """[]"""



def search_qwiki(what):
    """Search qwiki to make sure we'll get a result in our embed.
    Success is a string (of json), failure is None.
    The results of this search are discarded after checking"""
    query = urllib.urlencode({'q':what.title()})
    result = urllib.urlopen(QWIKI_QUERY + query).read()
    return result


def get_qwiki_embed(what):
    """Get the title for the first relevant article on Qwiki, or None"""
    result = None
    text = search_qwiki(what)
    json = simplejson.loads(text)
    if len(json) > 0:
        result = json[0]['embed_url']
    return result


def query_from_url(url):
    """Get the query from the end of the url"""
    return url.split('/')[-1]


def render_qwiki_embed(what):
    """Make the oembed code for the Qwiki"""
    url = "http://www.qwiki.com/q/#!/%s" % \
        urllib.quote_plus(query_from_url(what))
    return '<a class="oembed" href="%s" data-oembed-type="video">%s</a>' %\
        (url, url)
