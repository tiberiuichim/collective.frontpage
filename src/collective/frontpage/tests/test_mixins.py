# -*- coding: utf-8 -*-

from collective.frontpage.browser.mixins import SectionsViewMixin
from collective.frontpage.testing import COLLECTIVE_FRONTPAGE_FUNCTIONAL_TESTING  # noqa: 501
from collective.frontpage.testing import COLLECTIVE_FRONTPAGE_INTEGRATION_TESTING  # noqa: 501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class MixinsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_FRONTPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.frontpage = api.content.create(
            self.portal, "Frontpage", "my-frontpage", "My Frontpage"
        )
        self.section = api.content.create(
            self.frontpage, "Teaser", "my-section", "My Teaser"
        )
        self.view = self.section.restrictedTraverse("teaser_default")

    def test_text_color_image(self):
        self.assertTrue(self.view())
        self.section.background_image = "not null"
        self.assertEqual("#FFF", self.view.text_color(self.section))

    def test_text_color(self):
        self.section.background_color = "rgb(255,255,255)"
        self.assertEqual("#000", self.view.text_color(self.section))
        self.section.background_color = "rgb(0,0,0)"
        self.assertEqual("#FFF", self.view.text_color(self.section))

    def test_button_text_color(self):
        self.section.primary_color = "rgb(255,255,255)"
        self.assertEqual("#000", self.view.button_text_color(self.section))
        self.section.primary_color = "rgb(0,0,0)"
        self.assertEqual("#FFF", self.view.button_text_color(self.section))

    def test_contrasting_text_color(self):
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color("#000"))
        self.assertEqual(
            "#000", SectionsViewMixin._contrasting_text_color("#FFF"))
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color("#000000"))
        self.assertEqual(
            "#000", SectionsViewMixin._contrasting_text_color("#FFFFFF"))
        self.assertEqual(
            "#000", SectionsViewMixin._contrasting_text_color(
                "rgb(255,255,255)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color("rgb(0,0,0)"))
        self.assertEqual(
            "#000", SectionsViewMixin._contrasting_text_color(
                "rgba(255,255,255, 0.5)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color(
                "rgba(0,0,0, 0.5)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color("rgba(0,0,0, 0)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color(
                "rgba(0,0,0, 0.1)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color(
                "rgba(0,0,0, 1.0)")
        )
        self.assertEqual(
            "#FFF", SectionsViewMixin._contrasting_text_color("rgba(0,0,0, 1)")
        )


class MixinsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_FRONTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
