# -*- coding: utf-8 -*-

"""
Tests for Note class and its components
"""

import pytest
from books.note_book.note.note import Title, Text, Tag, Tags, Note
from books.note_book.error.exceptions import NoteTitleMandatory, NoteTextMandatory, TagValueCannotBeEmpty


class TestTitle:
    """Tests for the Title class"""

    def test_title_initialization(self, sample_title):
        """Test Title initialization"""
        title = Title(sample_title)
        assert title.value == sample_title
        assert str(title) == sample_title

    def test_title_empty_string(self):
        """Test Title with empty string"""
        with pytest.raises(NoteTitleMandatory):
            Title("")

    def test_title_whitespace_only(self):
        """Test Title with whitespace only"""
        # Implementation doesn't validate whitespace-only strings
        title = Title("   ")
        assert title.value == "   "
        assert str(title) == "   "


class TestText:
    """Tests for the Text class"""

    def test_text_initialization(self, sample_text):
        """Test Text initialization"""
        text = Text(sample_text)
        assert text.value == sample_text
        assert str(text) == sample_text

    def test_text_empty_string(self):
        """Test Text with empty string"""
        with pytest.raises(NoteTextMandatory):
            Text("")

    def test_text_whitespace_only(self):
        """Test Text with whitespace only"""
        # Implementation doesn't validate whitespace-only strings
        text = Text("   ")
        assert text.value == "   "
        assert str(text) == "   "


class TestTag:
    """Tests for the Tag class"""

    def test_tag_initialization(self):
        """Test Tag initialization"""
        tag = Tag("test")
        assert tag.value == "test"
        assert str(tag) == "test"

    def test_tag_empty_string(self):
        """Test Tag with empty string"""
        with pytest.raises(TagValueCannotBeEmpty):
            Tag("")

    def test_tag_whitespace_only(self):
        """Test Tag with whitespace only"""
        # Implementation doesn't validate whitespace-only strings
        tag = Tag("   ")
        assert tag.value == "   "
        assert str(tag) == "   "


class TestTags:
    """Tests for the Tags class"""

    def test_tags_initialization_empty(self):
        """Test Tags initialization with no arguments"""
        tags = Tags()
        assert len(tags) == 0
        assert str(tags) == ""

    def test_tags_initialization_with_tags(self):
        """Test Tags initialization with tag arguments"""
        tags = Tags("tag1", "tag2", "tag3")
        assert len(tags) == 3
        assert "tag1" in tags
        assert "tag2" in tags
        assert "tag3" in tags
        assert str(tags) == "tag1, tag2, tag3"

    def test_tags_iteration(self):
        """Test Tags iteration"""
        tags = Tags("tag1", "tag2", "tag3")
        iterated_tags = list(tags)
        assert len(iterated_tags) == 3
        # Tags iteration returns Tag objects, not strings
        iterated_tag_strings = [str(tag) for tag in iterated_tags]
        assert "tag1" in iterated_tag_strings
        assert "tag2" in iterated_tag_strings
        assert "tag3" in iterated_tag_strings

    def test_tags_contains(self):
        """Test Tags contains operation"""
        tags = Tags("tag1", "tag2", "tag3")
        assert "tag1" in tags
        assert "tag4" not in tags

    def test_tags_add(self):
        """Test Tags addition"""
        tags1 = Tags("tag1", "tag2")
        tags2 = Tags("tag3", "tag4")
        
        # Test __add__
        tags3 = tags1 + tags2
        assert len(tags3) == 4
        assert "tag1" in tags3
        assert "tag2" in tags3
        assert "tag3" in tags3
        assert "tag4" in tags3
        
        # Test __radd__
        tags4 = Tags("tag5") + tags1
        assert len(tags4) == 3
        assert "tag1" in tags4
        assert "tag2" in tags4
        assert "tag5" in tags4
        
        # Test __iadd__
        tags1 += tags2
        assert len(tags1) == 4
        assert "tag1" in tags1
        assert "tag2" in tags1
        assert "tag3" in tags1
        assert "tag4" in tags1

    def test_tags_sub(self):
        """Test Tags subtraction"""
        tags1 = Tags("tag1", "tag2", "tag3", "tag4")
        tags2 = Tags("tag2", "tag4")
        
        # Test __sub__
        tags3 = tags1 - tags2
        assert len(tags3) == 2
        assert "tag1" in tags3
        assert "tag3" in tags3
        assert "tag2" not in tags3
        assert "tag4" not in tags3
        
        # Test __rsub__
        tags4 = Tags("tag1", "tag5") - tags1
        assert len(tags4) == 1
        assert "tag5" in tags4
        assert "tag1" not in tags4
        
        # Test __isub__
        tags1 -= tags2
        assert len(tags1) == 2
        assert "tag1" in tags1
        assert "tag3" in tags1
        assert "tag2" not in tags1
        assert "tag4" not in tags1


class TestNote:
    """Tests for the Note class"""

    def test_note_initialization_minimal(self, sample_title, sample_text):
        """Test Note initialization with minimal parameters"""
        note = Note(sample_title, sample_text)
        assert note.title == sample_title
        assert note.text == sample_text
        assert len(note.tags) == 0
        assert str(note)  # Check that __str__ doesn't raise exceptions

    def test_note_initialization_with_tags(self, sample_title, sample_text, sample_tags):
        """Test Note initialization with tags"""
        note = Note(sample_title, sample_text, sample_tags)
        assert note.title == sample_title
        assert note.text == sample_text
        assert note.tags_number == len(sample_tags)
        for tag in sample_tags:
            assert tag in note.tags
        assert str(note)  # Check that __str__ doesn't raise exceptions

    def test_note_empty_title(self, sample_text):
        """Test Note with empty title"""
        with pytest.raises(NoteTitleMandatory):
            Note("", sample_text)

    def test_note_empty_text(self, sample_title):
        """Test Note with empty text"""
        with pytest.raises(NoteTextMandatory):
            Note(sample_title, "")

    def test_edit_title(self, sample_title, sample_text):
        """Test editing the title"""
        note = Note(sample_title, sample_text)
        new_title = "New Title"
        note.edit_title(new_title)
        assert note.title == new_title

    def test_edit_text(self, sample_title, sample_text):
        """Test editing the text"""
        note = Note(sample_title, sample_text)
        new_text = "New text content."
        note.edit_text(new_text)
        assert note.text == new_text

    def test_tags_operations(self, sample_title, sample_text):
        """Test tags operations"""
        note = Note(sample_title, sample_text)
        
        # Add tags
        note.add_tags("tag1", "tag2", "tag3")
        assert note.tags_number == 3
        assert "tag1" in note.tags
        assert "tag2" in note.tags
        assert "tag3" in note.tags
        
        # Add duplicate tags (should not add duplicates)
        note.add_tags("tag1", "tag4")
        assert note.tags_number == 4
        assert "tag4" in note.tags
        
        # Delete tags
        note.delete_tags("tag1", "tag3")
        assert note.tags_number == 2
        assert "tag2" in note.tags
        assert "tag4" in note.tags
        assert "tag1" not in note.tags
        assert "tag3" not in note.tags
        
        # Replace tags
        note.replace_tags("tag5", "tag6")
        assert note.tags_number == 2
        assert "tag5" in note.tags
        assert "tag6" in note.tags
        assert "tag2" not in note.tags
        assert "tag4" not in note.tags
        
        # Check if tag exists
        assert note.is_tag_exist("tag5")
        assert not note.is_tag_exist("tag1")

    def test_tags_number(self, sample_title, sample_text):
        """Test tags_number property"""
        note = Note(sample_title, sample_text)
        assert note.tags_number == 0
        
        note.add_tags("tag1", "tag2", "tag3")
        assert note.tags_number == 3
        
        note.delete_tags("tag1")
        assert note.tags_number == 2

    def test_parse_text_for_hashtags(self, sample_title):
        """Test parsing hashtags from text"""
        # Text with hashtags
        text_with_hashtags = "This is a #test text with #multiple #hashtags."
        note = Note(sample_title, text_with_hashtags, hashtags=True)
        
        # Check that hashtags were parsed
        assert note.tags_number == 3
        assert "test" in note.tags
        assert "multiple" in note.tags
        assert "hashtags" in note.tags
        
        # Text without hashtags
        text_without_hashtags = "This is a text without hashtags."
        note2 = Note(sample_title, text_without_hashtags, hashtags=True)
        assert note2.tags_number == 0
        
        # Disable hashtag parsing
        note3 = Note(sample_title, text_with_hashtags, hashtags=False)
        assert note3.tags_number == 0
        
        # Test the class method directly
        parsed_tags = Note.parse_text_for_hashtags(text_with_hashtags)
        assert len(parsed_tags) == 3
        assert "test" in parsed_tags
        assert "multiple" in parsed_tags
        assert "hashtags" in parsed_tags