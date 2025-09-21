from .py_loader import PythonLoader


def get_loader(loader_type: str):
    if loader_type == "python":
        return PythonLoader()
    raise ValueError(f"Loader desconhecido: {loader_type}")
