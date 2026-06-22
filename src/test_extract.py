import unittest
from extract import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_base(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/fejio.png)"
        )
        self.assertListEqual(
            matches,
            [("image", "https://i.imgur.com/fejio.png")]
        )

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "![rick roll](https://i.imgur.com/rick.gif) and ![obi wan](https://i.imgur.com/obi.jpeg)"
        )
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/rick.gif"),
                ("obi wan", "https://i.imgur.com/obi.jpeg")
            ]
        )

    def test_no_images(self):
        matches = extract_markdown_images("This is text with no markdown images.")
        self.assertListEqual(
            matches,
            []
        )

    def test_ignores_links(self):
        matches = extract_markdown_images(
            "This is a [link](https://www.boot.dev), not an image"
        )
        self.assertListEqual(
            matches,
            []
        )

    def test_image_mixed_with_link(self):
        matches = extract_markdown_images(
            "![alt text](https://example.com/image.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            matches,
            [("alt text", "https://example.com/image.png")]
        )

    def test_empty_alt_text(self):
        matches = extract_markdown_images(
            "![](https://example.com/image.png)"
        )
        self.assertListEqual(
            matches,
            [("", "https://example.com/image.png")]
        )

class TextExtractMarkdownLinks(unittest.TestCase):
    def test_base(self):
        matches = extract_markdown_links("This is text with a [exampl](https://example.com)")
        self.assertListEqual(
            matches,
            [("exampl", "https://example.com")]
        )

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "[example](example.com) and [google](google.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("example", "example.com"),
                ("google", "google.com")
            ]
        )

    def test_no_links(self):
        matches = extract_markdown_links("This text contains no links")
        self.assertListEqual(
            matches,
            []
        )

    def test_ignore_images(self):
        matches = extract_markdown_links("This is an ![image](https://www.google.com/image.jpg), not a link")
        self.assertListEqual(
            matches,
            []

        )

    def test_link_mixed_with_image(self):
        matches = extract_markdown_links(
            "![alt text](https://example.com/image.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            matches,
            [("link", "https://example.com")]
        )

    def test_empty_display_text(self):
        matches = extract_markdown_links(
            "[](google.com)"
        )
        self.assertListEqual(
            matches,
            [("", "google.com")]
        )
