#!/usr/bin/env python3
"""
Tortoise-TTS Batch Inference Script
This script processes text files from data/texts/<emotion>/*.txt and generates audio using Tortoise-TTS
Output: outputs/tortoise/<emotion>/tortoise-<emotion>-XX.wav
"""

import os
import sys
from pathlib import Path

# Get the project root directory (parent of scripts)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_TEXTS_DIR = PROJECT_ROOT / "data" / "texts"
DATA_REFS_DIR = PROJECT_ROOT / "data" / "references"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tortoise"
TORTOISE_MODEL_DIR = PROJECT_ROOT / "models" / "tortoise-tts"

# Add Tortoise-TTS to path
sys.path.insert(0, str(TORTOISE_MODEL_DIR))

try:
    import torch
    import torchaudio
    from tortoise.api import TextToSpeech
    from tortoise.utils.audio import load_audio
except ImportError as e:
    print(f"Error importing Tortoise-TTS: {e}")
    print("Make sure Tortoise-TTS is installed and you're in the correct conda environment")
    sys.exit(1)

# Configuration
emotions = ['happy', 'sad', 'angry', 'tired', 'excited', 'neutral']

# Check directories
if not TORTOISE_MODEL_DIR.exists():
    print(f"Error: Tortoise-TTS model directory not found at {TORTOISE_MODEL_DIR}")
    sys.exit(1)

if not DATA_TEXTS_DIR.exists():
    print(f"Error: Texts directory not found at {DATA_TEXTS_DIR}")
    sys.exit(1)

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Tortoise-TTS model
print("Loading Tortoise-TTS model...")
try:
    tts = TextToSpeech()
    print("Tortoise-TTS model loaded successfully!")
except Exception as e:
    print(f"Error loading Tortoise-TTS model: {e}")
    sys.exit(1)

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
    voice_samples = None
    conditioning_latents = None
    
    if ref_audio_file.exists():
        print(f"  Using reference audio: {ref_audio_file}")
        try:
            # Load reference audio (Tortoise expects 22050 Hz)
            audio = load_audio(str(ref_audio_file), 22050)
            voice_samples = [audio]
        except Exception as e:
            print(f"  Warning: Failed to load reference audio: {e}")
            print(f"  Using random conditioning latents instead")
            voice_samples = None
    else:
        print(f"  No reference audio found, using random conditioning latents")
    
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
        # e.g., 01.txt -> tortoise-happy-01.wav
        input_stem = text_file.stem  # Get filename without extension
        output_filename = f"tortoise-{emotion}-{input_stem}.wav"
        output_path = emotion_output_dir / output_filename
        
        print(f"  Generating: {text_file.name} -> {output_filename}")
        print(f"    Text: {gen_text[:50]}...")
        
        try:
            # Generate audio using Tortoise-TTS
            gen, _ = tts.tts_with_preset(
                gen_text,
                voice_samples=voice_samples,
                conditioning_latents=conditioning_latents,
                preset='fast',  # Use 'fast' preset for quicker generation
                k=1,
                verbose=False,
                use_deterministic_seed=None,
                return_deterministic_state=True,
            )
            
            # Save audio (Tortoise outputs at 24kHz)
            if isinstance(gen, list):
                gen = gen[0]
            torchaudio.save(
                str(output_path),
                gen.squeeze(0).cpu(),
                24000  # Tortoise-TTS sample rate
            )
            print(f"    ✓ Saved: {output_path}")
        except Exception as e:
            print(f"    ✗ Error generating {output_filename}: {e}")

print("\nTortoise-TTS batch processing completed!")
