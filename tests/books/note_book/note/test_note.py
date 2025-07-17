import unittest
from books.note_book.note.note import Note


class TestNote(unittest.TestCase):
    def setUp(self):
        # Create a basic note for testing
        self.note = Note(
            title="Meeting Notes",
            text="Discuss project timeline and deliverables #work #meeting",
            tags=["important"]
        )

    def test_init(self):
        # Test initialization with all parameters
        self.assertEqual(self.note.title, "Meeting Notes")
        self.assertEqual(self.note.text, "Discuss project timeline and deliverables #work #meeting")
        self.assertIn("important", self.note.tags)
        self.assertIn("work", self.note.tags)  # Should be extracted from text
        self.assertIn("meeting", self.note.tags)  # Should be extracted from text
        self.assertEqual(self.note.tags_number, 3)
        
        # Test initialization with minimal parameters
        note_minimal = Note(
            title="Simple Note",
            text="Just a simple note without tags"
        )
        self.assertEqual(note_minimal.title, "Simple Note")
        self.assertEqual(note_minimal.text, "Just a simple note without tags")
        self.assertEqual(note_minimal.tags_number, 0)
        
        # Test initialization with hashtags disabled
        note_no_hashtags = Note(
            title="No Hashtags",
            text="This note has #tags but they won't be extracted",
            hashtags=False
        )
        self.assertEqual(note_no_hashtags.title, "No Hashtags")
        self.assertEqual(note_no_hashtags.text, "This note has #tags but they won't be extracted")
        self.assertEqual(note_no_hashtags.tags_number, 0)

    def test_str(self):
        # Test string representation with tags
        expected = "Note title: Meeting Notes; text: Discuss project timeline and deliverables #work #meeting; tags: important, meeting, work"
        self.assertEqual(str(self.note), expected)
        
        # Test string representation without tags
        note_no_tags = Note(
            title="No Tags",
            text="This note has no tags"
        )
        expected = "Note title: No Tags; text: This note has no tags"
        self.assertEqual(str(note_no_tags), expected)

    def test_parse_text_for_hashtags(self):
        # Test hashtag extraction
        text = "This is a #test note with #multiple #hashtags"
        hashtags = Note.parse_text_for_hashtags(text)
        self.assertEqual(set(hashtags), {"test", "multiple", "hashtags"})
        
        # Test with no hashtags
        text = "This note has no hashtags"
        hashtags = Note.parse_text_for_hashtags(text)
        self.assertEqual(hashtags, [])
        
        # Test with duplicate hashtags
        text = "This note has #duplicate and #duplicate hashtags"
        hashtags = Note.parse_text_for_hashtags(text)
        self.assertEqual(hashtags, ["duplicate"])  # Should be deduplicated
        
        # Test with empty text
        hashtags = Note.parse_text_for_hashtags("")
        self.assertEqual(hashtags, [])
        
        # Test with None
        hashtags = Note.parse_text_for_hashtags(None)
        self.assertEqual(hashtags, [])

    def test_add_tags(self):
        # Test adding new tags
        self.note.add_tags("urgent", "project")
        self.assertEqual(self.note.tags_number, 5)
        self.assertIn("urgent", self.note.tags)
        self.assertIn("project", self.note.tags)
        
        # Test adding existing tags (should be deduplicated)
        self.note.add_tags("important", "work")
        self.assertEqual(self.note.tags_number, 5)  # No change in count
        
        # Test adding empty or None tags (should be ignored)
        self.note.add_tags("", None)
        self.assertEqual(self.note.tags_number, 5)  # No change in count

    def test_delete_tags(self):
        # Test deleting existing tags
        self.note.delete_tags("important", "work")
        self.assertEqual(self.note.tags_number, 1)
        self.assertNotIn("important", self.note.tags)
        self.assertNotIn("work", self.note.tags)
        self.assertIn("meeting", self.note.tags)  # Should still be present
        
        # Test deleting non-existent tags (should not affect existing tags)
        self.note.delete_tags("nonexistent")
        self.assertEqual(self.note.tags_number, 1)  # No change in count
        
        # Test deleting empty or None tags (should be ignored)
        self.note.delete_tags("", None)
        self.assertEqual(self.note.tags_number, 1)  # No change in count

    def test_replace_tags(self):
        # Test replacing all tags
        self.note.replace_tags("new", "tags")
        self.assertEqual(self.note.tags_number, 2)
        self.assertIn("new", self.note.tags)
        self.assertIn("tags", self.note.tags)
        self.assertNotIn("important", self.note.tags)
        self.assertNotIn("work", self.note.tags)
        self.assertNotIn("meeting", self.note.tags)
        
        # Test replacing with empty list
        self.note.replace_tags()
        self.assertEqual(self.note.tags_number, 0)
        
        # Test replacing with duplicate, empty, or None tags
        self.note.replace_tags("tag1", "tag1", "", None, "tag2")
        self.assertEqual(self.note.tags_number, 2)
        self.assertIn("tag1", self.note.tags)
        self.assertIn("tag2", self.note.tags)

    def test_is_tag_exist(self):
        # Test checking for existing tags
        self.assertTrue(self.note.is_tag_exist("important"))
        self.assertTrue(self.note.is_tag_exist("work"))
        self.assertTrue(self.note.is_tag_exist("meeting"))
        
        # Test checking for non-existent tags
        self.assertFalse(self.note.is_tag_exist("nonexistent"))
        
        # Test checking for empty or None tags
        self.assertFalse(self.note.is_tag_exist(""))
        self.assertFalse(self.note.is_tag_exist(None))


if __name__ == "__main__":
    unittest.main()