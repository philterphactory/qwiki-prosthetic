from django.test import TestCase

import prosthetic

LOCATION = "The Coffee Bean & Tea Leaf"
BAD_LOCATION = "&$%$#$^"

TEXT = "This is a place"
THUMB_URL = "http://url.com/img.jpg"
EMBED = "http://www.qwiki.com/q/#!/"

class QwikiTest(TestCase):
    def setUp(self):
        self.qwiki = prosthetic.Qwiki(None)

    def test_search_qwiki(self):
        result = self.qwiki.search_qwiki(LOCATION)
        self.failIfEqual(result, prosthetic.QWIKI_FOUND_NOTHING)
        self.failUnless("Coffee" in result)
        self.failUnless(self.qwiki.qwiki_has_results_for(LOCATION))

    def test_search_qwiki_fail(self):
        result = self.qwiki.search_qwiki(BAD_LOCATION)
        self.failUnlessEqual(result, prosthetic.QWIKI_FOUND_NOTHING)
        self.failIf(self.qwiki.qwiki_has_results_for(BAD_LOCATION))

    def test_search_render_qwiki(self):
        rendered = self.qwiki.qwiki_embed(LOCATION)
        self.failUnless(EMBED in rendered)
