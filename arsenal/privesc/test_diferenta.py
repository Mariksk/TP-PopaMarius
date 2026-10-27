from arsenal.privesc.diferenta import cai


def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert acum - baza == {"c"}


def test_citeste_cai_din_captura():
    assert cai("arsenal/privesc/start/baza_suid.txt") == {
        "/usr/bin/passwd",
        "/usr/bin/sudo",
        "/usr/bin/chsh",
        "/usr/bin/chfn",
        "/usr/bin/newgrp",
        "/usr/bin/gpasswd",
        "/bin/mount",
        "/bin/umount",
        "/bin/su",
    }
