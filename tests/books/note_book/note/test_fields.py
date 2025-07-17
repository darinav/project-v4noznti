import unittest
from books.note_book.note.note import Title, Text, Tag, Tags
from books.note_book.error.exceptions import NoteTitleMandatory, NoteTextMandatory, TagValueCannotBeEmpty


class TestTitle(unittest.TestCase):
    def test_valid_title(self):
        # Test valid title
        title = Title("My Note")
        self.assertEqual(str(title), "My Note")
        
        title = Title("A")  # Single character should be valid
        self.assertEqual(str(title), "A")

    def test_invalid_title(self):
        # Test empty title
        with self.assertRaises(NoteTitleMandatory):
            Title("")
        
        # Test None title
        with self.assertRaises(NoteTitleMandatory):
            Title(None)


class TestText(unittest.TestCase):
    def test_valid_text(self):
        # Test valid text
        text = Text("This is a note text")
        self.assertEqual(str(text), "This is a note text")
        
        text = Text("A")  # Single character should be valid
        self.assertEqual(str(text), "A")

    def test_invalid_text(self):
        # Test empty text
        with self.assertRaises(NoteTextMandatory):
            Text("")
        
        # Test None text
        with self.assertRaises(NoteTextMandatory):
            Text(None)


class TestTag(unittest.TestCase):
    def test_valid_tag(self):
        # Test valid tag
        tag = Tag("work")
        self.assertEqual(str(tag), "work")
        
        tag = Tag("A")  # Single character should be valid
        self.assertEqual(str(tag), "A")

    def test_invalid_tag(self):
        # Test empty tag
        with self.assertRaises(TagValueCannotBeEmpty):
            Tag("")
        
        # Test None tag
        with self.assertRaises(TagValueCannotBeEmpty):
            Tag(None)


class TestTags(unittest.TestCase):
    def test_init(self):
        # Test initialization with tags
        tags = Tags("work", "important", "meeting")
        self.assertEqual(len(tags), 3)
        
        # Test initialization with no tags
        tags = Tags()
        self.assertEqual(len(tags), 0)
        
        # Test initialization with duplicate tags (should be deduplicated)
        tags = Tags("work", "work", "important")
        self.assertEqual(len(tags), 2)
        
        # Test initialization with None or empty tags (should be ignored)
        tags = Tags("work", None, "", "important")
        self.assertEqual(len(tags), 2)

    def test_str(self):
        # Test string representation
        tags = Tags("work", "important", "meeting")
        # Tags should be sorted alphabetically
        self.assertEqual(str(tags), "important, meeting, work")
        
        # Test with no tags
        tags = Tags()
        self.assertEqual(str(tags), "")

    def test_iter(self):
        # Test iteration
        tags = Tags("work", "important", "meeting")
        tag_list = [str(tag) for tag in tags]
        # Order is not guaranteed in iteration
        self.assertEqual(set(tag_list), {"work", "important", "meeting"})

    def test_contains(self):
        # Test contains
        tags = Tags("work", "important", "meeting")
        self.assertIn("work", tags)
        self.assertIn("important", tags)
        self.assertIn("meeting", tags)
        self.assertNotIn("nonexistent", tags)

    def test_len(self):
        # Test length
        tags = Tags("work", "important", "meeting")
        self.assertEqual(len(tags), 3)
        
        tags = Tags()
        self.assertEqual(len(tags), 0)

    def test_add(self):
        # Test adding tags
        tags1 = Tags("work", "important")
        tags2 = Tags("meeting", "deadline")
        
        # Add tags2 to tags1
        result = tags1 + tags2
        self.assertEqual(len(result), 4)
        self.assertIn("work", result)
        self.assertIn("important", result)
        self.assertIn("meeting", result)
        self.assertIn("deadline", result)
        
        # Test right add (radd)
        tags3 = Tags("project")
        result = tags3 + tags1
        self.assertEqual(len(result), 3)
        self.assertIn("project", result)
        self.assertIn("work", result)
        self.assertIn("important", result)

    def test_sub(self):
        # Test subtracting tags
        tags1 = Tags("work", "important", "meeting", "deadline")
        tags2 = Tags("meeting", "deadline")
        
        # Subtract tags2 from tags1
        result = tags1 - tags2
        self.assertEqual(len(result), 2)
        self.assertIn("work", result)
        self.assertIn("important", result)
        self.assertNotIn("meeting", result)
        self.assertNotIn("deadline", result)
        
        # Test right subtract (rsub)
        tags3 = Tags("work", "project")
        result = tags3 - tags1
        self.assertEqual(len(result), 1)
        self.assertIn("project", result)
        self.assertNotIn("work", result)


if __name__ == "__main__":
    unittest.main()