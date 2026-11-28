# Making a Release

Adapted from Cyberbots' `release/RELEASING.md` (commit `bac6fde`, itself from
XvSF ← MSHvSF `7d4c587`) for Night Warriors Deluxe (`REL-001`). These steps
cover the prepared 0.2.0 candidate. Version 0.1.0 is already published, and
the `v0.2.0` tag is pushed. The GitHub Release and asset upload are pending.

The agent prepares, verifies, commits and pushes the tracked release records.
The user publishes on github.com as `princeendo`, because `gh` on this machine
is signed in as the work account, which this project never uses.

## Before You Start

- [x] Every open task in `TASKS.md` is done or explicitly deferred by the user
      by name. On 2026-11-27, the user deferred `COV-001`, `REF-001` and
      `REF-003` from v0.2.0; they remain open for later work.
- [x] The release image cold-booted in Mednafen (`EXP-0050`, `EXP-0051`). The
      user accepted assuming hardware parity for the 4 MiB animation path;
      real Saturn timing, stability and sprite behavior remain unverified
      (`EXP-0051`).
- [ ] `git status` is clean, on `main`, and up to date with `origin/main`.
- [ ] `git config user.email` prints
      `13876322+princeendo@users.noreply.github.com`.
- [ ] The untouched US image matches `references/saturn_us/README.md` (Redump
      disc 5836), and `xdelta3 -V` reports 3.2.2.

## 1. Candidate and Patch

The combined candidate is `build/next_release_candidate`. Its Track 1 SHA-256
must match `d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d`
in `build_manifest.json`.

```bash
./invenv.sh python -m tools.disc.make_patch --built-dir build/next_release_candidate \
  --stem night_warriors_deluxe --out-dir build/release/v0.2.0-patch/patch \
  --record release/night_warriors_deluxe_v0.2.0.json
./invenv.sh python -m tools.disc.make_patch --built-dir build/next_release_candidate \
  --stem night_warriors_deluxe --out-dir build/release/v0.2.0-patch-again/patch
cmp build/release/v0.2.0-patch/patch/night_warriors_deluxe.Track1.xdelta \
    build/release/v0.2.0-patch-again/patch/night_warriors_deluxe.Track1.xdelta
```

The patch is metadata-recorded in `release/night_warriors_deluxe_v0.2.0.json`;
patch bytes stay under ignored `build/` paths.

## 2. Zip, Repeat, and Apply Check

```bash
V="US Enhanced, US Original, JP Enhanced, and JP Original (switched in OPTION MODE)"
./invenv.sh python -m tools.release.make_zips 0.2.0 build/release/v0.2.0 --kinds xdelta \
  --records release --patches build/release/v0.2.0-patch \
  --variant night_warriors_deluxe_v0.2.0 patch "$V"
./invenv.sh python -m tools.release.make_zips 0.2.0 build/release/v0.2.0-again --kinds xdelta \
  --records release --patches build/release/v0.2.0-patch \
  --variant night_warriors_deluxe_v0.2.0 patch "$V"
shasum -a 256 build/release/v0.2.0/*.zip build/release/v0.2.0-again/*.zip
cmp build/release/v0.2.0/night_warriors_deluxe_0.2.0_xdelta.zip \
    build/release/v0.2.0-again/night_warriors_deluxe_0.2.0_xdelta.zip
./invenv.sh python -m tools.release.check_zips 0.2.0 build/release/v0.2.0 \
  local/rel/v0.2.0-check --kinds xdelta \
  --expect d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d
```

The two zips must be byte-identical, and applying the packaged patch to the
untouched US Track 1 must reproduce the candidate hash. The prepared zip is
66,177 bytes with SHA-256
`45f8ea0883b7db1dc97cacaa2bf8357113a817a738d23abf408a533d5369bef5`.

## 3. Release and Posting Notes

Use `release/notes_v0.2.0.md` as the GitHub release description. A Reddit post
draft is in `release/reddit_post_v0.2.0.md`. The download zip is not committed.

## 4. Records and Git

- Record the session and verification outputs in `research_log.md`.
- Update `TASKS.md` only when acceptance criteria are met and any open tasks
  are either completed or explicitly deferred by the user by name.
- Keep `README.md` clear about which version is published versus prepared.
- Stage only tracked files: never commit the zip, `.xdelta`, images, or
  `local_agent_guidance.md` (`AGENTS.md` rule 21).
- The release decision, package metadata, and notes are committed and pushed;
  the annotated tag is pushed separately. The user publishes the GitHub
  Release and uploads the zip below.

## 5. Publish (User, on github.com)

| Do this | What you should see |
| --- | --- |
| Open the repository's Releases page, click **Draft a new release**, and choose tag `v0.2.0`. | The `v0.2.0` tag is selected. |
| Set the title to `0.2.0: Four Editions` and paste `release/notes_v0.2.0.md` into the description. | The release notes render cleanly. |
| Upload `build/release/v0.2.0/night_warriors_deluxe_0.2.0_xdelta.zip` and publish. | The zip appears under Assets. |

After publication, verify the asset size and `sha256:` digest through the
public GitHub API against the local zip.
