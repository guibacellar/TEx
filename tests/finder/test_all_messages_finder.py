import asyncio
import unittest
from configparser import ConfigParser

from TEx.finder.all_messages_finder import AllMessagesFinder


class AllMessagesFinderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_find_true(self):
        """Test the always true return."""

        target: AllMessagesFinder = AllMessagesFinder(config=self.config)

        loop = asyncio.get_event_loop()
        tasks = target.find(raw_text='foo'), target.find(raw_text=None)

        h_result_content, h_result_none = loop.run_until_complete(
            asyncio.gather(*tasks)
        )

        self.assertTrue(h_result_content)
        self.assertTrue(h_result_none)

