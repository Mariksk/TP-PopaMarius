import pytest

from arsenal.aparare.detector import suspecti
from arsenal.aparare.parse_auth import pe_ip


def test_pragul_taie():
    esecuri = [
        {"user": "ana", "ip": "203.0.113.9"},
        {"user": "ion", "ip": "198.51.100.7"},
        {"user": "ion", "ip": "203.0.113.9"},
    ]
    counts = pe_ip(esecuri)
    assert counts == {"203.0.113.9": 2, "198.51.100.7": 1}
    assert suspecti(counts, 2) == [("203.0.113.9", 2)]


def test_prag_invalid():
    with pytest.raises(ValueError, match="prag invalid"):
        suspecti({}, 0)
