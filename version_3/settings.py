"""Settings."""

from pathlib import Path
from os.path import join

BASE_DIR = Path(__file__).resolve(strict=True).parent
IMAGES_DIR = join(BASE_DIR, 'images')
SOUNDS_DIR = join(BASE_DIR, 'sounds')
