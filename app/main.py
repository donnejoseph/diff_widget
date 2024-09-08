from PySide6.QtWidgets import QApplication

from app.widgets.code_compare_widget import CodeCompareWidget

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Пример кода для сравнения
    user_code = """def say_hello(name):
    name = name
    hello = 'hello '
    message = hello + name
    return message"""

    ai_code = """def say_hello(name):
    return f"hello {name}"""

    # Создаем и показываем виджет сравнения
    widget = CodeCompareWidget(user_code, ai_code)
    widget.show()
    sys.exit(app.exec())