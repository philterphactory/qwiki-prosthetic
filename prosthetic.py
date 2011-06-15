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

from base_prosthetic import Prosthetic
from django.template.loader import render_to_string
import logging
import random
import re
import time
import urllib


QWIKI_QUERY = "http://embed-api.qwiki.com/api/v1/search.json?count=1&"
QWIKI_FOUND_NOTHING = """[]"""


class NoLocationFoundException(Exception):
    """An exception to mark that no location was found. As its name implies."""
    pass


class Qwiki(Prosthetic):
    """A simple demo prosthetic that blogs the weavr's experience of
    qwiki articles related to it's location."""

    def is_awake(self, state):
        return state['awake']

    def should_post(self, state):
        return self.is_awake(state)

    def get_location(self, state):
        """Get the Weavr's current location.
           Raises NoLocatioNFoundException if no current location."""
        # find recent location
        locations = self.get("/1/weavr/location/")['locations']
        if len(locations) == 0:
            logging.info("no location found")
            raise NoLocatioNFoundException()
        location = locations[0]
        return location

    def search_qwiki(self, what):
        """Search qwiki to make sure we'll get a result in our embed.
           Success is a string (of json), failure is None.
           The results of this search are discarded after checking"""
        query = urllib.urlencode({'q':what})
        result = urllib.urlopen(QWIKI_QUERY + query).read()
        return result

    def qwiki_has_results_for(self, what):
        """Check whether qwiki has any results for the given terms"""
        response = self.search_qwiki(what)
        result = response != QWIKI_FOUND_NOTHING
        return result 

    def qwiki_embed(self, query):
        #FIXME: urlencode the query
        url = "http://www.qwiki.com/q/#!/%s" % query
        return '<a class="oembed" href="%s" data-oembed-type="video">%s</a>' %\
            (url, url)

    def get_location_search(self, state):
        location = self.get_location(state)
        return location['city'] or location['region']

    def get_media_keywords_search(self, state):
        return random.choice(state['combined_keywords'].split())

    def get_title(self, what):
        return "Curious about %s" % what

    def act(self, force=False):
        result = "Error"
        logging.info("Starting")
        try:
            state = self.get("/1/weavr/state/")
            logging.info("Got state")
            if self.should_post(state):
                what = self.get_media_keywords_search(state)
                logging.info("should search for: %s" % what)
                if self.qwiki_has_results_for(what):
                    logging.info("posting new qwiki: %s" % what)
                    embed = self.qwiki_embed(what)
                    self.post("/1/weavr/post/", {
                            "category":"article",
                            "title":self.get_title(what),
                            "body":embed,
                            "keywords":state["emotion"],
                            })
                    result = "posted qwiki about %s" % what
                else:
                    logging.info("Nothing found for %s" % what)
                    result = "no results searching qwiki for %s" % what
        except NoLocationFoundException, e:
            logging.info("No location found")
            logging.info(str(e))
            pass
        except Exception, e:
            logging.error("Exception in qwiki prosthetic:\n%s" % str(e))
        return result