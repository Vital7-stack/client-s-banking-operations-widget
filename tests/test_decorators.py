import pytest
import os
from decorators import log

@pytest.fixture
def cleanup_log_file():
    """Фикстура для очистки тестового лог‑файла после тестов."""
    yield
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

def test_log_to_console(capsys):
    """Тест логирования в консоль."""
    @log()
    def test_function(x, y):
        return x + y

    test_function(1, 2)
    captured = capsys.readouterr()
    assert "test_function called with: 1, 2" in captured.out
    assert "test_function ok" in captured.out

def test_log_to_file(cleanup_log_file):
    """Тест логирования в файл."""
    @log(filename="test_log.txt")
    def test_function(a, b):
        return a * b

    test_function(3, 4)

    with open("test_log.txt", 'r', encoding='utf-8') as f:
        content = f.read()
    assert "test_function called with: 3, 4" in content
    assert "test_function ok" in content

def test_log_with_error(capsys):
    """Тест логирования ошибки в консоль."""
    @log()
    def problematic_function(x):
        if x < 0:
            raise ValueError("Negative value not allowed")
        return x ** 2

    with pytest.raises(ValueError):
        problematic_function(-1)

    captured = capsys.readouterr()
    assert "problematic_function error: ValueError" in captured.out
    assert "Inputs: (-1,), {}" in captured.out

def test_log_with_kwargs(capsys):
    """Тест логирования функции с именованными аргументами."""
    @log()
    def complex_function(a, b=10, c="default"):
        return f"{a}-{b}-{c}"

    complex_function(5, c="custom")
    captured = capsys.readouterr()
    # Проверяем только ключевые части сообщения, игнорируя временную метку
    assert "complex_function called with: 5, c='custom'" in captured.out
    assert "complex_function ok" in captured.out

def test_log_empty_args(capsys):
    """Тест логирования функции без аргументов."""
    @log()
    def no_args_function():
        return "Hello"

    no_args_function()
    captured = capsys.readouterr()
    assert "no_args_function called with:" in captured.out
    assert "no_args_function ok" in captured.out

@pytest.mark.parametrize("filename", ["log1.txt", "subdir/log2.txt"])
def test_log_different_filenames(filename, tmp_path):
    """Тест с разными именами файлов."""
    if "/" in filename:
        subdir = filename.split("/")[0]
        os.makedirs(tmp_path / subdir, exist_ok=True)
        full_path = tmp_path / filename
    else:
        full_path = tmp_path / filename

    @log(filename=str(full_path))
    def temp_function():
        return 42

    temp_function()

    assert full_path.exists()
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "temp_function called with:" in content
    assert "temp_function ok" in content