from random import randint

from django.test import TestCase

from ..models import Correspondent, Document, Tag
from ..signals import document_consumption_finished


class TestMatching(TestCase):

    def _test_matching(self, text, algorithm, true, false):
        for klass in (Tag, Correspondent):
            instance = klass.objects.create(
                name=str(randint(10000, 99999)),
                match=text,
                matching_algorithm=getattr(klass, algorithm)
            )
            for string in true:
                self.assertTrue(instance.matches(string))
            for string in false:
                self.assertFalse(instance.matches(string))

    def test_match_all(self):

        self._test_matching(
            "alpha charlie gamma",
            "MATCH_ALL",
            ("I have alpha, charlie, and gamma in me",),
            (
                "I have alpha in me",
                "I have charlie in me",
                "I have gamma in me",
                "I have alpha and charlie in me",
                "I have alphas, charlie, and gamma in me",
                "I have alphas in me",
                "I have bravo in me",
            )
        )

        self._test_matching(
            "12 34 56",
            "MATCH_ALL",
            (
                "I have 12 34, and 56 in me",
            ),
            (
                "I have 12 in me",
                "I have 34 in me",
                "I have 56 in me",
                "I have 12 and 34 in me",
                "I have 120, 34, and 56 in me",
                "I have 123456 in me",
                "I have 01234567 in me",
            )
        )

    def test_match_any(self):

        self._test_matching(
            "alpha charlie gamma",
            "MATCH_ANY",
            (
                "I have alpha in me",
                "I have charlie in me",
                "I have gamma in me",
                "I have alpha, charlie, and gamma in me",
                "I have alpha and charlie in me",
            ),
            (
                "I have alphas in me",
                "I have bravo in me",
            )
        )

        self._test_matching(
            "12 34 56",
            "MATCH_ANY",
            (
                "I have 12 in me",
                "I have 34 in me",
                "I have 56 in me",
                "I have 12 and 34 in me",
                "I have 12, 34, and 56 in me",
                "I have 120, 34, and 56 in me",
            ),
            (
                "I have 123456 in me",
                "I have 01234567 in me",
            )
        )

    def test_match_literal(self):

        self._test_matching(
            "alpha charlie gamma",
            "MATCH_LITERAL",
            (
                "I have 'alpha charlie gamma' in me",
            ),
            (
                "I have alpha in me",
                "I have charlie in me",
                "I have gamma in me",
                "I have alpha and charlie in me",
                "I have alpha, charlie, and gamma in me",
                "I have alphas, charlie, and gamma in me",
                "I have alphas in me",
                "I have bravo in me",
            )
        )

        self._test_matching(
            "12 34 56",
            "MATCH_LITERAL",
            (
                "I have 12 34 56 in me",
            ),
            (
                "I have 12 in me",
                "I have 34 in me",
                "I have 56 in me",
                "I have 12 and 34 in me",
                "I have 12 34, and 56 in me",
                "I have 120, 34, and 560 in me",
                "I have 120, 340, and 560 in me",
                "I have 123456 in me",
                "I have 01234567 in me",
            )
        )

    def test_match_regex(self):

        self._test_matching(
            "alpha\w+gamma",
            "MATCH_REGEX",
            (
                "I have alpha_and_gamma in me",
                "I have alphas_and_gamma in me",
            ),
            (
                "I have alpha in me",
                "I have gamma in me",
                "I have alpha and charlie in me",
                "I have alpha,and,gamma in me",
                "I have alpha and gamma in me",
                "I have alpha, charlie, and gamma in me",
                "I have alphas, charlie, and gamma in me",
                "I have alphas in me",
            )
        )


class TestApplications(TestCase):
    """
    We make use of document_consumption_finished, so we should test that it's
    doing what we expect wrt to tag & correspondent matching.
    """

    def setUp(self):
        TestCase.setUp(self)
        self.doc_contains = Document.objects.create(
            content="I contain the keyword.", file_type="pdf")

    def test_tag_applied_any(self):
        t1 = Tag.objects.create(
            name="test", match="keyword", matching_algorithm=Tag.MATCH_ANY)
        document_consumption_finished.send(
            sender=self.__class__, document=self.doc_contains)
        self.assertTrue(list(self.doc_contains.tags.all()) == [t1])

    def test_tag_not_applied(self):
        Tag.objects.create(
            name="test", match="no-match", matching_algorithm=Tag.MATCH_ANY)
        document_consumption_finished.send(
            sender=self.__class__, document=self.doc_contains)
        self.assertTrue(list(self.doc_contains.tags.all()) == [])

    def test_correspondent_applied(self):
        correspondent = Correspondent.objects.create(
            name="test",
            match="keyword",
            matching_algorithm=Correspondent.MATCH_ANY
        )
        document_consumption_finished.send(
            sender=self.__class__, document=self.doc_contains)
        self.assertTrue(self.doc_contains.correspondent == correspondent)

    def test_correspondent_not_applied(self):
        Tag.objects.create(
            name="test",
            match="no-match",
            matching_algorithm=Correspondent.MATCH_ANY
        )
        document_consumption_finished.send(
            sender=self.__class__, document=self.doc_contains)
        self.assertEqual(self.doc_contains.correspondent, None)
