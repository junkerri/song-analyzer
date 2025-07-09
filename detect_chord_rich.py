import sys
from rich import print
from rich.table import Table
import essentia
import essentia.standard as es

# Check if the user gave a filename
if len(sys.argv) < 2:
    print("[bold red]Error:[/] You must provide a WAV file path.")
    print("Usage: python detect_chord_rich.py /path/to/your/file.wav")
    sys.exit(1)

# Get the filename from the command-line arguments
filename = sys.argv[1]

# Load the WAV file
audio = es.MonoLoader(filename=filename)()

# Estimate key and scale
key, scale, strength = es.KeyExtractor()(audio)

# Estimate BPM
rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
bpm, beats, _, _, _ = rhythm_extractor(audio)

# Create a Rich table
table = Table(title="🎸 Guitar Analysis Results")

table.add_column("Property", style="cyan bold")
table.add_column("Value", style="magenta")

table.add_row("File", filename)
table.add_row("Detected Key", f"[bold yellow]{key}[/]")
table.add_row("Scale", scale)
table.add_row("Strength", f"{strength:.3f}")
table.add_row("Detected BPM", f"{bpm:.2f}")

print(table)
