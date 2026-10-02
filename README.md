# PepesFamily looping video

Delivered outputs (video/mp4):

| File | Dimensions | Duration | Rate | Size |
| --- | --- | --- | --- | --- |
| artifacts/video.mp4 | 1920 × 1080 | 10.000 s | 30 fps / 300 frames | 4.65 MB |
| artifacts/video-square.mp4 | 1080 × 1080 | 10.000 s | 30 fps / 300 frames | 2.62 MB |

Both files use browser-compatible H.264 High, yuv420p, AAC-LC stereo at 48 kHz, and MP4 faststart. AAC contains only digital silence, resolving the silent-audio request alongside the acceptance requirement for an AAC stream. Each output is below 15 MB. Exact sizes and checksums are in validation.json.

Original flat illustration with seven rear-view frogs, two rows, instrument panels, terminal typing, scrolling trades, percentage coins, bounce and arm animations, and the requested logo. The square export is the centre 1080 pixels of the landscape scene; all seven characters and all terminal content remain visible. Peripheral instrument columns are cropped. Motion cycles over ten seconds; the final frame deliberately repeats the opening state. Checks confirm the decoded first and last frames are byte-identical, not just the source artwork.

Typography uses the included IBM Plex Mono regular font with expanded character spacing. Display slogans and brand are uppercase. Terminal commands and the URL preserve the exact lower-case strings supplied in the brief, which conflicts with its general all-uppercase direction. The specified frog clothing colours and soft red sell line are retained despite the general single-accent direction. There is no audible soundtrack, real person, facial feature, external brand, price, or additional on-screen copy.

Validation: ffprobe checks codec, dimensions, frame rate, frame count and duration; ffmpeg decodes boundary frames for matching MD5 hashes, and the entire AAC stream for all-zero sample verification. MP4 atom inspection verifies moov precedes mdat. Selected artwork frames were inspected locally. Actual X upload and playback in individual browsers were not tested; network platforms may recompress the files and change exact frame equality.

Source: source/render.py constructs the original artwork and streams frames directly to ffmpeg; source/check.py performs verification and updates validation.json. Run both from the repository root with Python 3.12 and ffmpeg/ffprobe available. Pillow is included as an ordinary offline wheel for CPython 3.12 / Linux x86_64 and automatically extracted under /tmp if unavailable. Rendering needs no network or node_modules. IBM's font license is included alongside the font; Pillow's licenses are included inside its wheel. Other Python platforms require their own compatible Pillow installation.

The named MP4 outputs are left untracked for separate artifact upload.
