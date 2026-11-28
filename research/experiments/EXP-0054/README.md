# EXP-0054: Track 2 on both retail discs

- Task: COV-001 (FILE-10)
- Status: DONE
- Confidence: CONFIRMED for the track contents

## Observation and Hypothesis

The source manifests show nonzero samples on JP Track 2 and all zeros on
US Track 2. The hypothesis was that the JP samples held a spoken warning
about playing a data disc.

## Controlled Comparison

The disc region was the only variable. Both CUEs declare Track 2 as
`AUDIO` in a `BINARY` file with a 150-sector pregap. Decode the same
index range (`INDEX 01` through end of track) as stereo 44.1 kHz signed
16-bit little-endian PCM. The stock Mednafen 1.32.1 image reader
(`CDAccess_Image.cpp`, CUE `BINARY` branch and raw audio sector read)
also reads these sectors without swapping the sample bytes.

Inputs were the untouched JP 1M `T-1202G` (Redump 3677) and US `T-1208H`
(Redump 5836) images. The Track 2 inputs matched the
[JP](../../../references/saturn_jp/README.md) and
[US](../../../references/saturn_us/README.md) SHA-256 manifests.

## Result

| Release | Track 2 file bytes | Playable duration | Nonzero stereo frames | Local WAV size and SHA-256 |
| --- | ---: | ---: | ---: | --- |
| JP 1M | 3,880,800 | 20.000 s | 640,599 | 3,528,078 bytes, `1fbd747b37fe72cabc8af58877a9f98359e52817f136fbee117579cc97fb3c5f` |
| US | 1,766,352 | 8.013 s | 0 | 1,413,630 bytes, `d7b4df114d7f22e9914db6174f1a855d1d77456c2936f1a3421627370d8919b4` |

The WAV payloads matched the original track bytes after the pregap. The
JP signal starts at stereo frame 16,069 and ends before frame 824,639,
about 0.364–18.699 s after `INDEX 01`. The US pregap and playable audio
are all zero.

Offline Japanese speech recognition and English translation both
identified two repetitions of the warning. The speaker identifies the CD
as software for the Sega Saturn and compatible game systems and asks the
listener to avoid playing it because it contains game data. The model
made phonetic errors in the hardware phrase. The result identifies the
warning's subject and purpose. Exact wording and any in-game CD audio
calls were outside this comparison.

## Reproduction

Tools were FFmpeg/ffprobe 9.0.1, Python 3.13.13 for the WAV comparison,
and Python 3.12.13 with faster-whisper 1.2.1 and CTranslate2 4.8.3 for the
local speech check. The cached Systran faster-whisper-small snapshot was
`536b0662742c02347bc0e980a01041f333bce120` with model SHA-256
`3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671`.
The first WAV transcription attempt hit a PyAV 19.0.1 keyword
incompatibility. Passing FFmpeg-decoded samples to the same model worked.

```sh
mkdir -p local/exp0054
ffmpeg -nostdin -v error -n -f s16le -ar 44100 -ac 2 \
  -i "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M) (Track 2).bin" \
  -ss 2 local/exp0054/jp-track2.wav
ffmpeg -nostdin -v error -n -f s16le -ar 44100 -ac 2 \
  -i "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA) (Track 2).bin" \
  -ss 2 local/exp0054/us-track2.wav
shasum -a 256 local/disc_images/*/*\(Track\ 2\).bin local/exp0054/*.wav
```

Using `./invenv.sh python`, read the WAV payload with
`wave.readframes(wave.getnframes())`, compare it to the track bytes at
`150 * 2352` onward, and count each four-byte group that contains a
nonzero sample. For recognition, send the JP WAV through
`ffmpeg -nostdin -v error -i local/exp0054/jp-track2.wav -ar 16000 -ac 1 -f f32le pipe:1`.
Interpret its output as a NumPy `<f4` array. Load the local snapshot with
`WhisperModel(snapshot, device="cpu", compute_type="int8", cpu_threads=4, local_files_only=True)`
and run `model.transcribe(audio, task=task, beam_size=5, vad_filter=True)`
once each with `task="transcribe"` and `task="translate"`. The local
speech output SHA-256 is
`14bf5299caa4a4e285c602c47c6e8762fc978ef7f2a0d5c4c272c9036a1700b6`.
