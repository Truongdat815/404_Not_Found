"""
Unit tests cho file handler
"""

import pytest
from pathlib import Path
from app.utils.file_handler import extract_text_from_file, save_uploaded_file, cleanup_file


def test_extract_text_txt(tmp_path):
    """Test extract text từ .txt file"""
    # Tạo test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test SRS document.\nRequirement 1: Test requirement.")
    
    # Extract text
    text = extract_text_from_file(str(test_file))
    assert "test SRS" in text
    assert "Requirement 1" in text


def test_extract_text_invalid_file():
    """Test extract text với file không tồn tại"""
    with pytest.raises(FileNotFoundError):
        extract_text_from_file("nonexistent.txt")


def test_extract_text_unsupported_type(tmp_path):
    """Test extract text với file type không support"""
    test_file = tmp_path / "test.pdf"
    test_file.write_text("test")
    
    with pytest.raises(ValueError):
        extract_text_from_file(str(test_file))


def test_cleanup_file(tmp_path):
    """Test cleanup file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    
    assert test_file.exists()
    cleanup_file(str(test_file))
    assert not test_file.exists()


@pytest.mark.skip(reason="Requires python-docx và test .docx file")
def test_extract_text_docx():
    """Test extract text từ .docx file"""
    # Skip nếu không có test .docx file
    pass

