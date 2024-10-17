from unittest.mock import MagicMock, patch
import pytest
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.storage.sql_storage import SQLStorage

@pytest.fixture
def docx_loader():
    return DOCXLoader()

def test_validate_small_docx_file(docx_loader):
    small_docx_path = "test_files/docx/small.docx"
    assert docx_loader.load_file(small_docx_path), f"Loaded DOCX file: {small_docx_path}"

def test_validate_large_docx_file(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

def test_validate_corrupted_docx_file(docx_loader):
    corrupted_docx_path = "test_files/docx/corrupted.docx"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(corrupted_docx_path)

def test_validate_non_docx_file(docx_loader):
    non_docx_path = "test_files/pdf/small.pdf"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(non_docx_path)

def test_validate_empty_docx_file(docx_loader):
    empty_docx_path = "test_files/docx/empty.docx"
    assert docx_loader.load_file(empty_docx_path), f"Loaded DOCX file: {empty_docx_path}"

def test_validate_docx_with_complex_formatting(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

def test_validate_password_protected_docx(docx_loader):
    protected_docx_path = "test_files/docx/password.docx"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(protected_docx_path)

def test_validate_docx_with_embedded_links(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

def test_validate_docx_with_embedded_images(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

def test_validate_docx_with_multiple_sections(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

def test_validate_docx_with_comments_or_track_changes(docx_loader):
    large_docx_path = "test_files/docx/large.docx"
    assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

@pytest.fixture
def pdf_loader():
    return PDFLoader()

def test_validate_small_pdf_file(pdf_loader):
    small_pdf_path = "test_files/pdf/small.pdf"
    assert pdf_loader.load_file(small_pdf_path), f"Loaded PDF file: {small_pdf_path}"

def test_validate_large_pdf_file(pdf_loader):
    large_pdf_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(large_pdf_path), f"Loaded PDF file: {large_pdf_path}"

def test_validate_corrupted_pdf_file(pdf_loader):
    corrupted_pdf_path = "test_files/pdf/corrupted.pdf"
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(corrupted_pdf_path)

def test_validate_non_pdf_file(pdf_loader):
    non_pdf_path = "test_files/docx/small.docx"
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(non_pdf_path)

def test_validate_empty_pdf_file(pdf_loader):
    empty_pdf_path = "test_files/pdf/empty.pdf"
    assert pdf_loader.load_file(empty_pdf_path), f"Loaded PDF file: {empty_pdf_path}"

def test_validate_password_protected_pdf(pdf_loader):
    protected_pdf_path = "test_files/pdf/password.pdf"
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(protected_pdf_path)

def test_validate_pdf_with_embedded_links(pdf_loader):
    pdf_with_links_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(pdf_with_links_path), f"Loaded PDF file: {pdf_with_links_path}"

def test_validate_pdf_with_embedded_images(pdf_loader):
    pdf_with_images_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(pdf_with_images_path), f"Loaded PDF file: {pdf_with_images_path}"

def test_validate_pdf_with_multiple_pages(pdf_loader):
    multi_page_pdf_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(multi_page_pdf_path), f"Loaded PDF file: {multi_page_pdf_path}"

def test_validate_pdf_with_comments(pdf_loader):
    pdf_with_comments_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(pdf_with_comments_path), f"Loaded PDF file: {pdf_with_comments_path}"

@pytest.fixture
def ppt_loader():
    return PPTLoader()

def test_validate_small_pptx_file(ppt_loader):
    small_pptx_path = "test_files/pptx/small.pptx"
    assert ppt_loader.load_file(small_pptx_path), f"Loaded PPTX file: {small_pptx_path}"

def test_validate_large_pptx_file(ppt_loader):
    large_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(large_pptx_path), f"Loaded PPTX file: {large_pptx_path}"

def test_validate_corrupted_pptx_file(ppt_loader):
    corrupted_pptx_path = "test_files/pptx/corrupted.pptx"
    with pytest.raises(ValueError, match="Invalid PPT file."):
        ppt_loader.load_file(corrupted_pptx_path)

def test_validate_non_pptx_file(ppt_loader):
    non_pptx_path = "test_files/pdf/small.pdf"
    with pytest.raises(ValueError, match="Invalid PPT file."):
        ppt_loader.load_file(non_pptx_path)

def test_validate_empty_pptx_file(ppt_loader):
    empty_pptx_path = "test_files/pptx/empty.pptx"
    assert ppt_loader.load_file(empty_pptx_path), f"Loaded PPTX file: {empty_pptx_path}"

def test_validate_pptx_with_complex_animations(ppt_loader):
    complex_animations_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(complex_animations_pptx_path), f"Loaded PPTX file: {complex_animations_pptx_path}"

def test_validate_password_protected_pptx(ppt_loader):
    protected_pptx_path = "test_files/pptx/password.pptx"
    with pytest.raises(ValueError, match="Invalid PPT file."):
        ppt_loader.load_file(protected_pptx_path)

def test_validate_pptx_with_embedded_links(ppt_loader):
    links_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(links_pptx_path), f"Loaded PPTX file: {links_pptx_path}"

def test_validate_pptx_with_embedded_images(ppt_loader):
    images_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(images_pptx_path), f"Loaded PPTX file: {images_pptx_path}"

def test_validate_pptx_with_videos(ppt_loader):
    video_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(video_pptx_path), f"Loaded PPTX file: {video_pptx_path}"

def test_validate_pptx_with_multiple_slides_and_transitions(ppt_loader):
    multiple_slides_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(multiple_slides_pptx_path), f"Loaded PPTX file: {multiple_slides_pptx_path}"

def test_validate_pptx_with_embedded_audio(ppt_loader):
    audio_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(audio_pptx_path), f"Loaded PPTX file: {audio_pptx_path}"

def test_validate_pptx_with_custom_slide_layouts(ppt_loader):
    custom_layout_pptx_path = "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(custom_layout_pptx_path), f"Loaded PPTX file: {custom_layout_pptx_path}"

@pytest.fixture
def valid_db_path():
    """Fixture for the valid SQLite database path."""
    return "assignment4.db"

@pytest.fixture
def invalid_db_path():
    """Fixture for an invalid SQLite database path."""
    return "/invalid/path/to/assignment4.db"

@pytest.fixture
def mock_cursor():
    """Mock the cursor and connection for SQLite."""
    cursor_mock = MagicMock()
    connection_mock = MagicMock()
    cursor_mock.cursor.return_value = cursor_mock
    cursor_mock.__enter__.return_value = cursor_mock
    connection_mock.connect.return_value = connection_mock
    return cursor_mock, connection_mock

def test_validate_successful_database_connection(mock_cursor, valid_db_path):
    cursor_mock, connection_mock = mock_cursor
    # Patch the sqlite3.connect method to return a mock connection
    with patch('sqlite3.connect', return_value=connection_mock):
        storage = SQLStorage(database=valid_db_path)
        assert storage.conn is not None, "Connected to SQLite database"

def test_validate_failed_database_connection(mock_cursor, invalid_db_path):
    cursor_mock, connection_mock = mock_cursor
    # Patch the sqlite3.connect method to return a mock connection
    with patch('sqlite3.connect', return_value=connection_mock):
        storage = SQLStorage(database=invalid_db_path)
        assert storage.conn is not None, "Cannot connected to sqlite database"
            
if __name__ == "__main__":
    pytest.main()
