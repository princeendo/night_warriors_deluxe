"""Unpack the release zips and apply every patch to the untouched Track 1 (REL-001).

Copied into the Night Warriors Deluxe repository from the Cyberbots repository,
``tools/release/check_zips.py`` at commit ``bac6fde`` (Cyberbots copied and
rewrote XvSF ``9cb01ad`` ← MSHvSF ``7d4c587``). Changed: defaults target Night
Warriors Deluxe (US Saturn Track 1, ``night_warriors_deluxe`` prefix) and
xdelta-only releases (user decision 2026-11-25, ``REL-001``).

Prints the source track's SHA-256, then one line per patch: its file name and
the patched track's SHA-256. Every patch goes through ``xdelta3 -d``.

Run from the repository root, for example:

    ./invenv.sh python -m tools.release.check_zips 0.1.0 build/release/v0.1.0 \\
        local/rel/v0.1.0-check
"""

from __future__ import annotations

import argparse
import shutil
import zipfile
from collections.abc import Sequence
from pathlib import Path

from tools.disc.make_patch import SOURCE_DIR, TRACK01, decode
from tools.disc.patch_image import REPO_ROOT, sha256_file
from tools.release.make_zips import KINDS, PREFIX

WORK_ROOTS = ("build", "local")


def check_zips(
    zips: Path,
    version: str,
    source: Path,
    work: Path,
    prefix: str = PREFIX,
    xdelta: str = "xdelta3",
    kinds: Sequence[str] = KINDS,
) -> list[tuple[str, str]]:
    """(patch file name, patched track SHA-256) for every patch in the zips.

    ``work`` is replaced; the caller checks that it is safe to replace.
    """
    if work.exists():
        shutil.rmtree(work)
    for kind in kinds:
        with zipfile.ZipFile(zips / f"{prefix}_{version}_{kind}.zip") as bundle:
            bundle.extractall(work / "unz" / kind)
    out = work / "out.bin"
    results = []
    for patch in sorted((work / "unz" / "xdelta").glob("*.xdelta")):
        decode(xdelta, source, patch, out)
        results.append((patch.name, sha256_file(out)))
    out.unlink(missing_ok=True)
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("version", help="release version, e.g. 0.1.0")
    parser.add_argument("zips", type=Path, help="folder holding the release zips")
    parser.add_argument("work", type=Path, help="scratch folder (replaced)")
    parser.add_argument(
        "--source", type=Path, default=SOURCE_DIR / TRACK01, help="untouched track 1"
    )
    parser.add_argument("--prefix", default=PREFIX, help="zip file name prefix")
    parser.add_argument("--xdelta", default="xdelta3")
    parser.add_argument(
        "--expect", help="SHA-256 every patched track must have; exit 1 otherwise"
    )
    parser.add_argument(
        "--kinds", nargs="+", default=list(KINDS), choices=KINDS, help="formats"
    )
    args = parser.parse_args(argv)
    work = args.work.resolve()
    roots = [(REPO_ROOT / r).resolve() for r in WORK_ROOTS]
    if not any(root in work.parents for root in roots):
        parser.error(f"work folder must be under {' or '.join(map(str, roots))}")
    if shutil.which(args.xdelta) is None:
        parser.error(f"{args.xdelta} not found; install xdelta3")
    print(sha256_file(args.source))
    results = check_zips(
        args.zips,
        args.version,
        args.source,
        work,
        args.prefix,
        args.xdelta,
        args.kinds,
    )
    for name, digest in results:
        print(name, digest)
    if args.expect and (
        not results or any(digest != args.expect for _, digest in results)
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
