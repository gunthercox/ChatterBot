from unittest import TestCase

from chatterbot.storage import SQLStorageAdapter


class SQLTagPaginationTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False,
        )
        self.addCleanup(self.adapter.close)

    def test_statements_matching_multiple_tags_appear_once_across_pages(self):
        both = self.adapter.create(text='Both', tags=['red', 'blue'])
        red = self.adapter.create(text='Red', tags=['red'])
        blue = self.adapter.create(text='Blue', tags=['blue'])
        self.adapter.create(text='Unmatched', tags=['green'])

        for page_size in (1, 2, 3, 1000):
            with self.subTest(page_size=page_size):
                results = self.adapter.filter(
                    tags=['red', 'blue'], page_size=page_size, order_by=['id'],
                )
                self.assertEqual(
                    [statement.id for statement in results],
                    [both.id, red.id, blue.id],
                )

    def test_different_statements_with_the_same_text_are_preserved(self):
        first = self.adapter.create(text='Hello', tags=['red', 'blue'])
        second = self.adapter.create(text='Hello', tags=['red', 'blue'])

        results = self.adapter.filter(
            tags=['red', 'blue'], page_size=1, order_by=['id'],
        )

        self.assertEqual([statement.id for statement in results], [first.id, second.id])

    def test_tag_pagination_combines_with_other_statement_filters(self):
        self.adapter.create(text='Other', tags=['red', 'blue'], conversation='other')
        self.adapter.create(text='Exclude', tags=['red', 'blue'], conversation='current')
        kept = self.adapter.create(text='Keep', tags=['red', 'blue'], conversation='current')

        results = self.adapter.filter(
            tags=['red', 'blue'], page_size=1,
            conversation='current', exclude_text=['Exclude'],
        )

        self.assertEqual([statement.id for statement in results], [kept.id])
