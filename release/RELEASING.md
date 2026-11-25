# Making a Release

Adapted from Cyberbots' `release/RELEASING.md` (commit `bac6fde`, itself from
XvSF ← MSHvSF `7d4c587`) for Night Warriors Deluxe (`REL-001`). The examples
use `0.1.0`.

The agent does steps 1-6. You do steps 7-9 on github.com, because `gh` on this
machine is signed in as the work account, which this project never uses.

## Before You Start

- [ ] Every open task in `TASKS.md` is done, or explicitly deferred by the user.
- [ ] The release image has been cold-boot verified (Mednafen, or real hardware).
- [ ] `git status` is clean, on `main`, and up to date with `origin/main`.
- [ ] `git config user.email` prints
      `13876322+princeendo@users.noreply.github.com`.
- [ ] The untouched US image matches `references/saturn_us/README.md` (Redump
      disc 5836), and `xdelta3 -V` reports 3.2.2.

## 1. Rebuild and Check

```bash
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/us_edition
```

Track 1's SHA-256 in `build/us_edition/build_manifest.json` must match the
release target (`25e05ec14a258e7f2bea49e51023dfbf96c553aae688b67c5044728c4040f1be`
for `0.1.0`).

## 2. The Patch and Its Record

```bash
./invenv.sh python -m tools.disc.make_patch --built-dir build/us_edition \
  --stem night_warriors_deluxe --out-dir build/release/patch \
  --record release/night_warriors_deluxe.json
./invenv.sh python -m tools.disc.make_patch --built-dir build/us_edition \
  --stem night_warriors_deluxe --out-dir build/release/patch-again
cmp build/release/patch/night_warriors_deluxe.Track1.xdelta \
    build/release/patch-again/night_warriors_deluxe.Track1.xdelta
```

Both patches must be byte-identical. `release/night_warriors_deluxe.json` is
metadata only and is committed.

## 3. The Zip, Twice, and the Check

```bash
V="US Enhanced, US Original, and JP Original (switched in OPTION MODE)"
./invenv.sh python -m tools.release.make_zips 0.1.0 build/release/v0.1.0 --kinds xdelta \
  --patches build/release --variant night_warriors_deluxe patch "$V"
./invenv.sh python -m tools.release.make_zips 0.1.0 build/release/v0.1.0-again --kinds xdelta \
  --patches build/release --variant night_warriors_deluxe patch "$V"
shasum -a 256 build/release/v0.1.0/*.zip build/release/v0.1.0-again/*.zip
./invenv.sh python -m tools.release.check_zips 0.1.0 build/release/v0.1.0 local/rel/v0.1.0-check \
  --kinds xdelta --expect 25e05ec14a258e7f2bea49e51023dfbf96c553aae688b67c5044728c4040f1be
```

Both zips must hash identically, and applying the patch from the unpacked zip
to the untouched US Track 1 must match `--expect`.

## 4. The Notes

`release/notes_v0.1.0.md`: what changed, the zip with its size and SHA-256, how
to apply, and known limits.

## 5. Records

- `TASKS.md`: mark `REL-001` done with the zip hash and list deferred tasks.
- `research_log.md`: log the release session and verification outputs.
- `README.md`: link the release and summarize what changed.

Stage only tracked files: never commit the zip, the `.xdelta`, images, or
`local_agent_guidance.md` (`AGENTS.md` rule 21).

## 6. Commit, Tag, Push

```bash
git -c user.name=Colin -c user.email=13876322+princeendo@users.noreply.github.com commit ...
git tag -a v0.1.0 -m "Night Warriors Deluxe (Saturn) 0.1.0"
git push origin main v0.1.0
```

## 7-9. Publish (You, on github.com)

| Do this | What you should see |
| --- | --- |
| Open the repository's Releases page, click **Draft a new release**, and choose tag `v0.1.0`. | The `v0.1.0` tag is selected. |
| Set the title to `0.1.0` and paste the contents of `release/notes_v0.1.0.md` into the description. | The release notes render cleanly. |
| Drag in `build/release/v0.1.0/night_warriors_deluxe_0.1.0_xdelta.zip` and click **Publish release**. | The zip appears under Assets. |

Afterwards, the agent verifies the published asset's size and `sha256:` digest
through the public GitHub API against the local zip built in step 3.
