import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app.core.security import get_password_hash, verify_password


def test_password_hash_and_verify():
    senha = "senha_super_secreta"
    hash_gerado = get_password_hash(senha)
    assert hash_gerado != senha
    assert verify_password(senha, hash_gerado)
    assert not verify_password("errada", hash_gerado)
