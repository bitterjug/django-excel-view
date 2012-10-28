from django.test import TestCase

from excel_view import ColSpec, Col


class ColumnSpecificationTests(TestCase):

    def setUp(self):
        self.colspec = ColSpec(
                 Col("One"),
                 Col("Two", "a"),
                 Col("Three", "b", "c", reduce=sum),
                 Col("Four", 'd', 'e', reduce=" ".join))

    def test_headers(self):
        self.assertListEqual(
                self.colspec.headers(),
                ["One", "Two", "Three", "Four"])

    def test_inputs(self):
        self.assertListEqual(
                self.colspec.inputs(),
                ["One", "a", "b", "c", "d", "e"])

    def test_values(self):
        context = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': "foo",
            'e': "bar",
            'One': 6}
        self.assertListEqual(
                self.colspec.values(context),
                [6, 1, 5, "foo bar"])

    def test_fn(self):
        def inc(x):
            return x + 1
        self.colspec = ColSpec(Col('Header', 'key', function=inc))
        self.assertEqual(self.colspec.values({'key': 1}), [2])

    def test_default(self):
        self.colspec = ColSpec(Col('Header', 'key', default=7))
        self.assertEqual(self.colspec.values({}), [7])

    def test_default_and_fn(self):
        def inc(x):
            return x + 1
        colspec = ColSpec(
                Col('Header', 'key', function=inc, default=4))
        self.assertEqual(colspec.values({}), [5])

    def test_related(self):
        colspec = ColSpec(
                Col("0", 'q'),
                Col("Aa", 'a__x'),
                Col("Ab", 'b__x'),
                Col("Ac", 'c__x', 'c__y'),
                Col("Aa2", 'a__y'))
        expected = set(['a', 'b', 'c'])
        self.assertSetEqual(
                expected.symmetric_difference(colspec.related()), set())
