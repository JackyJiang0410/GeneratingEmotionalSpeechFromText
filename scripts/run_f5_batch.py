#!/usr/bin/env python3
"""
F5-TTS Batch Inference Script
This script processes text files from data/texts/<emotion>/*.txt and generates audio using F5-TTS
Output: outputs/f5/<emotion>/f5-<emotion>-XX.wav
"""

import os
import sys
from pathlib import Path
from importlib.resources import files as resource_files

# Ensure pydub uses ffmpeg instead of torchcodec
# Set FFMPEG_BINARY environment variable if ffmpeg is installed via homebrew
if os.path.exists("/opt/homebrew/bin/ffmpeg"):
    os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"
elif os.path.exists("/usr/local/bin/ffmpeg"):
    os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"

# Get the project root directory (parent of scripts)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_TEXTS_DIR = PROJECT_ROOT / "data" / "texts"
DATA_REFS_DIR = PROJECT_ROOT / "data" / "references"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "f5"
F5_MODEL_DIR = PROJECT_ROOT / "models" / "F5-TTS"

# Add F5-TTS to path
sys.path.insert(0, str(F5_MODEL_DIR / "src"))

try:
    from f5_tts.api import F5TTS
except ImportError as e:
    print(f"Error importing F5-TTS: {e}")
    print("Make sure F5-TTS is installed and you're in the correct conda environment")
    sys.exit(1)

# Configuration
emotions = ['happy', 'sad', 'angry', 'tired', 'excited', 'neutral']

# Check directories
if not F5_MODEL_DIR.exists():
    print(f"Error: F5-TTS model directory not found at {F5_MODEL_DIR}")
    sys.exit(1)

if not DATA_TEXTS_DIR.exists():
    print(f"Error: Texts directory not found at {DATA_TEXTS_DIR}")
    sys.exit(1)

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize F5-TTS model
print("Loading F5-TTS model...")
try:
    f5tts = F5TTS()
    print("F5-TTS model loaded successfully!")
except Exception as e:
    print(f"Error loading F5-TTS model: {e}")
    sys.exit(1)

# Default reference audio (fallback if no emotion-specific reference exists)
default_ref_audio = None
try:
    default_ref_audio = str(resource_files("f5_tts").joinpath("infer/examples/basic/basic_ref_en.wav"))
    if not os.path.exists(default_ref_audio):
        default_ref_audio = None
except Exception:
    default_ref_audio = None

# No-op progress wrapper to suppress progress bars
# The F5-TTS code uses progress.tqdm(), so we need a module-like object
class NoProgressModule:
    @staticmethod
    def tqdm(x, **kwargs):
        # Return iterable without progress display
        kwargs['disable'] = True
        from tqdm import tqdm
        return tqdm(x, **kwargs)

# Create a module-like object for progress
progress_module = NoProgressModule()

# Process each emotion
for emotion in emotions:
    emotion_text_dir = DATA_TEXTS_DIR / emotion
    
    if not emotion_text_dir.exists():
        print(f"Warning: {emotion_text_dir} not found, skipping emotion: {emotion}")
        continue
    
    if not emotion_text_dir.is_dir():
        print(f"Warning: {emotion_text_dir} is not a directory, skipping emotion: {emotion}")
        continue
    
    print(f"\nProcessing emotion: {emotion}")
    
    # Create output directory for this emotion
    emotion_output_dir = OUTPUT_DIR / emotion
    emotion_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for emotion-specific reference audio
    ref_audio_file = DATA_REFS_DIR / f"{emotion}_ref.wav"
    ref_text = ""
    
    if ref_audio_file.exists():
        print(f"  Using reference audio: {ref_audio_file}")
        # Try to get reference text (if exists as .txt file)
        ref_text_file = DATA_REFS_DIR / f"{emotion}_ref.txt"
        if ref_text_file.exists():
            with open(ref_text_file, 'r', encoding='utf-8') as f:
                ref_text = f.read().strip()
    else:
        # Use default reference audio if available
        if default_ref_audio:
            print(f"  Using default reference audio: {default_ref_audio}")
            ref_audio_file = default_ref_audio
            # Default reference text for basic_ref_en.wav
            ref_text = "Some call me nature, others call me mother nature."
        else:
            print(f"  Error: No reference audio found for {emotion} and no default available")
            print(f"  Skipping {emotion} - please provide {ref_audio_file} or ensure F5-TTS is properly installed")
            continue
    
    # Find all .txt files in the emotion directory
    text_files = sorted(emotion_text_dir.glob("*.txt"))
    
    if not text_files:
        print(f"  Warning: No .txt files found in {emotion_text_dir}, skipping")
        continue
    
    print(f"  Found {len(text_files)} text files")
    
    # Process each text file
    for text_file in text_files:
        # Read text from file
        with open(text_file, 'r', encoding='utf-8') as f:
            gen_text = f.read().strip()
        
        if not gen_text:
            print(f"  Warning: {text_file.name} is empty, skipping")
            continue
        
        # Generate output filename based on input filename
        # e.g., 01.txt -> f5-happy-01.wav
        input_stem = text_file.stem  # Get filename without extension
        output_filename = f"f5-{emotion}-{input_stem}.wav"
        output_path = emotion_output_dir / output_filename
        
        print(f"  Generating: {text_file.name} -> {output_filename}")
        print(f"    Text: {gen_text[:50]}...")
        
        try:
            f5tts.infer(
                ref_file=str(ref_audio_file),
                ref_text=ref_text,
                gen_text=gen_text,
                file_wave=str(output_path),
                show_info=lambda x: None,  # Suppress info messages
                progress=progress_module,  # Use our no-progress wrapper
            )
            print(f"    ✓ Saved: {output_path}")
        except Exception as e:
            print(f"    ✗ Error generating {output_filename}: {e}")

print("\nF5-TTS batch processing completed!")

