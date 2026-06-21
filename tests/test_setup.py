import sys


def test_core_imports() -> None:
    import cv2
    import fastapi
    import imagehash
    import qdrant_client
    import redis
    import requests
    import streamlit
    import torch
    import transformers

    assert sys.version_info >= (3, 10)
    assert cv2.__version__
    assert fastapi
    assert imagehash
    assert qdrant_client
    assert redis
    assert requests
    assert streamlit
    assert torch.__version__
    assert transformers.__version__
