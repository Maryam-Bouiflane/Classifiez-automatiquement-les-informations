import pytest
import os
from src.utils import save_object, load_object


def test_save_and_load_object(tmp_path):
    # Objet de test
    obj = {"a": 1, "b": [1, 2, 3]}

    file_path = tmp_path / "test.pkl"

    # Sauvegarde
    save_object(obj, file_path)

    # Chargement
    loaded_obj = load_object(file_path)

    # Vérification
    assert loaded_obj == obj


def test_save_creates_file(tmp_path):
    obj = [1, 2, 3]
    file_path = tmp_path / "file.pkl"

    save_object(obj, file_path)

    # Vérifie que le fichier existe
    assert os.path.exists(file_path)


def test_load_nonexistent_file():
    # Vérifie qu'une erreur est levée si le fichier n'existe pas
    with pytest.raises(FileNotFoundError):
        load_object("fake_file.pkl")


def test_save_and_load_complex_object(tmp_path):
    # Objet plus complexe
    obj = {
        "numbers": [1, 2, 3],
        "nested": {"x": 10},
        "text": "hello"
    }

    file_path = tmp_path / "complex.pkl"

    save_object(obj, file_path)
    loaded_obj = load_object(file_path)

    assert loaded_obj == obj