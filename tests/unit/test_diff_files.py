import struct

from tools.disc.diff_files import classify


def pack(*ws: int) -> bytes:
    return struct.pack(f">{len(ws)}I", *ws)


def test_same_size_pointer_and_content() -> None:
    a = pack(0x2FE64F22, 0x0608089A, 0x12345678, 0x06001000)
    b = pack(0x2FE64F22, 0x060808EA, 0x12345679, 0x06001050)
    r = classify(a, b)
    assert r["pointer_words"] == 2 and r["pointer_deltas"] == {"+0x50": 2}
    assert r["content_words"] == 1 and r["runs"] == 1 and r["differing_bytes"] == 3
    assert isinstance(r["code_start_a"], int) and r["code_start_a"] > 0


def test_insertion_counted() -> None:
    a = pack(1, 2, 3, 4, 5, 6)
    b = pack(1, 2, 3, 99, 98, 4, 5, 6)
    r = classify(a, b)
    assert r["inserted_words"] == 2 and r["deleted_words"] == 0 and r["runs"] == 1


def test_empty_file() -> None:
    assert classify(b"abcd", b"")["deleted_words"] == 1


def test_entry_table() -> None:
    from tools.disc.diff_files import entry_table

    data = pack(0x52A, 0x10, 0xFFFFFFFF, 0, 0x2FE64F22)
    assert entry_table(data) == (1, 1)
    assert entry_table(pack(0x2FE64F22, 0x6F03)) == (0, 0)
