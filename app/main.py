from PySide6.QtWidgets import QApplication
from app.widgets.code_compare_widget import CodeCompareWidget

if __name__ == "__main__":
    import sys

    app: QApplication = QApplication(sys.argv)

    # Example code for comparison
    user_code: str = """def say_hello(name):
    name = name
    hello = 'hello '
    message = hello + name
    return message"""

    ai_code: str = """def say_hello(name):
    return f'hello {name}'"""

    # Create and show the comparison widget
    widget: CodeCompareWidget = CodeCompareWidget(user_code, ai_code)
    widget.show()
    sys.exit(app.exec())
