# -*- coding: utf-8 -*-
from pserver.cms.testing import PserverCMSTestCase


class TestContent(PserverCMSTestCase):

    def test_content(self):
        self.assertEqual(
            self.layer.portal['news'].portal_type, 'Item')
        self.assertEqual(
            self.layer.portal['front-page'].portal_type, 'Document')
        self.assertEqual(
            self.layer.portal['events'].portal_type, 'Item')
