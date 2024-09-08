import pytest
from PySide6.QtCore import QSize, QEvent
from PySide6.QtWidgets import QApplication, QWidget

from app.widgets.line_number_area import LineNumberArea


@pytest.fixture(scope='module')
def app():
    """Fixture to create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def mock_editor(qtbot, app):
    """Fixture to create a mock editor widget for testing."""
    editor = QWidget()
    editor.line_number_area_width = lambda: 50  # Mock method to return a fixed width
    editor.line_number_area_paint_event = lambda event: None  # Mock method for painting
    qtbot.addWidget(editor)
    return editor


@pytest.fixture
def line_number_area(mock_editor, qtbot):
    """Fixture to create an instance of LineNumberArea for testing."""
    area = LineNumberArea(mock_editor)
    qtbot.addWidget(area)
    return area


def test_initialization(line_number_area, mock_editor):
    """Test if the LineNumberArea initializes correctly with the editor reference."""
    assert line_number_area.text_edit == mock_editor


def test_size_hint(line_number_area):
    """Test if the sizeHint method returns the correct size."""
    expected_size = QSize(50, 0)  # Based on the mock method return value
    assert line_number_area.sizeHint() == expected_size


def test_paint_event_handling(line_number_area, mock_editor):
    """Test if the paintEvent method correctly delegates to the editor's paint method."""
    event = QEvent(QEvent.Paint)

    # Use a flag to confirm if the mock method is called
    mock_called = False

    def mock_paint_event(event):
        nonlocal mock_called
        mock_called = True

    mock_editor.line_number_area_paint_event = mock_paint_event

    line_number_area.paintEvent(event)

    assert mock_called, "Expected the paint event to be delegated to the editor's paint method."
