import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    
    def test_extract_title(self):
        markdown = "# Title\n\nSome content"
        expected_title = "Title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_title(self):
        markdown = "Some content"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("Markdwon Error: No Title Detected!" in str(context.exception))
    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("Markdwon Error: No Title Detected!" in str(context.exception))
    def test_extract_title_multiple_titles(self):
        markdown = "# Title1\n\n# Title2\n\nSome content"
        expected_title = "Title1"
        self.assertEqual(extract_title(markdown), expected_title)
    def test_extract_title_no_newline(self):
        markdown = "# TitleSome content"
        expected_title = "TitleSome content"
        self.assertEqual(extract_title(markdown), expected_title)
    