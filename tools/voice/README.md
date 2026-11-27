# Kid voice recordings (ElevenLabs)

Voices: **Jett** (boy, pitch raised 1.12x in build) and **Fena** (girl). Free ElevenLabs plan, credited in Parent corner.

- `one.json` – the two main scripts (A: cheers/directions, B: question pieces, numbers, letters) and their clip keys
- `wchunks.json` / `words.json` – reading-game words, recorded in 3 parts per voice
- `missing.txt` – words still NOT recorded (≈175). Record these next month in both voices, then rebuild.
- `align.py` – cuts a long recording into clips by matching pause gaps to expected word lengths
- `build2.py <voice>` – builds `audio/voice-<voice>.mp3` + `.json` (clip map) from raw recordings in `raw/<voice>-A.mp3`, `-B.mp3`, `-W0..W2.mp3`

Recording tips: type items in ONE paragraph separated by " ... " (cheers) or ". " (words); a new line starts a separate block that isn't generated.
