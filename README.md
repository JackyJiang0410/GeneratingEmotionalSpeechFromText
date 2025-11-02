# Emo-TTS Benchmark

A performance evaluation project for comparing F5-TTS and Tortoise-TTS models on emotional speech synthesis tasks.

## Project Structure

```
emo-tts-benchmark/
├── models/
│   ├── f5-tts/          # F5-TTS model (git cloned)
│   └── tortoise-tts/    # Tortoise-TTS model (git cloned)
├── data/
│   ├── texts/           # Text files directory
│   │   ├── happy/        # Happy emotion texts
│   │   │   ├── 01.txt
│   │   │   ├── 02.txt
│   │   │   └── ...
│   │   ├── sad/          # Sad emotion texts
│   │   │   ├── 01.txt
│   │   │   ├── 02.txt
│   │   │   └── ...
│   │   ├── angry/        # Angry emotion texts
│   │   ├── tired/        # Tired emotion texts
│   │   ├── excited/      # Excited emotion texts
│   │   └── neutral/      # Neutral emotion texts
│   └── references/      # Emotional reference audio directory (optional, e.g., happy_ref.wav, sad_ref.wav...)
├── outputs/
│   ├── f5/              # F5-TTS output directory
│   │   ├── happy/
│   │   ├── sad/
│   │   └── ...
│   └── tortoise/         # Tortoise-TTS output directory
│       ├── happy/
│       ├── sad/
│       └── ...
├── scripts/
│   ├── run_f5_batch.py       # F5-TTS batch generation script
│   └── run_tortoise_batch.py  # Tortoise-TTS batch generation script
└── README.md
```

## Usage

### 1. Prepare Data

Create corresponding folders for each emotion under the `data/texts/` directory, and place multiple text files in each folder:

```
data/texts/
├── happy/
│   ├── 01.txt
│   ├── 02.txt
│   └── ...
├── sad/
│   ├── 01.txt
│   ├── 02.txt
│   └── ...
├── angry/
│   ├── 01.txt
│   └── ...
├── tired/
├── excited/
└── neutral/
```

Each `.txt` file should contain one line of text, which will be used to generate one audio file.

**Note:**
- File names can be in any format (e.g., `01.txt`, `file1.txt`, etc.)
- Output filenames will be generated based on input filenames (e.g., `01.txt` -> `f5-happy-01.wav`)

Optional: Place reference audio files in the `data/references/` directory (naming format: `<emotion>_ref.wav`), such as:
- `happy_ref.wav`
- `sad_ref.wav`
- ...

If reference audio does not exist, the scripts will use model default settings.

### 2. Run Batch Generation

Both scripts use Python format with unified execution:

#### F5-TTS

```bash
conda activate f5
python scripts/run_f5_batch.py
```

#### Tortoise-TTS

```bash
conda activate tortoise
python scripts/run_tortoise_batch.py
```

### 3. Output Format

Generated audio files will be named according to the following format:

- F5-TTS: `outputs/f5/<emotion>/f5-<emotion>-<filename>.wav`
- Tortoise-TTS: `outputs/tortoise/<emotion>/tortoise-<emotion>-<filename>.wav`

Where:
- `<emotion>`: Emotion name (happy, sad, angry, tired, excited, neutral)
- `<filename>`: Input text file name (without extension)

**Example:**
- Input: `data/texts/happy/01.txt`
- F5-TTS Output: `outputs/f5/happy/f5-happy-01.wav`
- Tortoise-TTS Output: `outputs/tortoise/happy/tortoise-happy-01.wav`

### 4. Comparison Analysis

Generated audio files follow a unified naming convention for easy comparison:

- The same input text file will generate corresponding audio files on both F5-TTS and Tortoise-TTS (with different prefixes)
- For example:
  - `outputs/f5/happy/f5-happy-01.wav`
  - `outputs/tortoise/happy/tortoise-happy-01.wav`

These two files are generated from the same input text file (`data/texts/happy/01.txt`), making it easy to compare the performance of both models.

## Important Notes

1. **Environment Requirements**:
   - F5-TTS needs to run in the corresponding conda environment
   - Tortoise-TTS needs to run in the corresponding conda environment

2. **Model Directories**:
   - Do not modify the contents of `models/f5-tts/` and `models/tortoise-tts/` directories
   - Scripts only read from these directories and will not modify them

3. **Reference Audio**:
   - Reference audio is optional; if not available, scripts will use model default settings
   - Reference audio format should be WAV

4. **Output Directory**:
   - Scripts will automatically create required output directories
   - If output files already exist, they will be overwritten

5. **Text Files**:
   - Each text file should contain one line of text
   - Empty files will be skipped
   - Filenames will be used to generate corresponding output filenames

## Script Description

### `run_f5_batch.py`

F5-TTS batch generation script (Python). This script:
- Iterates through all text files in `data/texts/<emotion>/` directories
- Checks for corresponding reference audio (`data/references/<emotion>_ref.wav`)
- Uses F5-TTS default reference audio if not available
- Generates speech for each text file, saved to `outputs/f5/<emotion>/f5-<emotion>-<filename>.wav`

### `run_tortoise_batch.py`

Tortoise-TTS batch generation script (Python). This script:
- Iterates through all text files in `data/texts/<emotion>/` directories
- Checks for corresponding reference audio (`data/references/<emotion>_ref.wav`)
- Uses random conditioning latents if reference audio is not available
- Generates speech for each text file, saved to `outputs/tortoise/<emotion>/tortoise-<emotion>-<filename>.wav`
- Uses 'fast' preset to speed up generation

## Supported Emotions

- `happy` - Happy
- `sad` - Sad
- `angry` - Angry
- `tired` - Tired
- `excited` - Excited
- `neutral` - Neutral

## Environment Setup

### F5-TTS Environment

1. Create conda environment:
```bash
conda create -n f5 python=3.11 -y
conda activate f5
```

2. Install PyTorch (for Apple Silicon):
```bash
pip install torch torchaudio
```

3. Install F5-TTS:
```bash
cd models/F5-TTS
pip install -e .
```

4. Important: Downgrade torchaudio to avoid torchcodec issues:
```bash
pip install "torchaudio<2.5"
```

### Tortoise-TTS Environment

1. Create conda environment:
```bash
conda create -n tortoise python=3.9 -y
conda activate tortoise
```

2. Install PyTorch (for Apple Silicon):
```bash
pip install torch torchaudio
```

3. Install Tortoise-TTS:
```bash
cd models/tortoise-tts
pip install -r requirements.txt
# or
pip install -e .
```

## Troubleshooting

### F5-TTS Issues

**Error: "TorchCodec is required for load_with_torchcodec"**
- Solution: Downgrade torchaudio to version < 2.5
- Command: `pip install "torchaudio<2.5"`

**Error: "'function' object has no attribute 'tqdm'"**
- Solution: The script has been updated with a proper progress wrapper. Make sure you're using the latest version.

### Tortoise-TTS Issues

**Error: "No module named 'tortoise'"**
- Solution: Ensure you're in the correct conda environment and Tortoise-TTS is installed

**Model download takes too long**
- Solution: First run will download models automatically. Ensure internet connection is available.

## License

This project is for research and educational purposes. Please refer to the respective model licenses:
- F5-TTS: See `models/F5-TTS/LICENSE`
- Tortoise-TTS: See `models/tortoise-tts/LICENSE`
