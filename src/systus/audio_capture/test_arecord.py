from systus.audio_capture.recorder import AudioRecorder

recorder = AudioRecorder()

print("🎤 Recording 5 seconds...")

path = recorder.record(5)

print("✅ File created:", path)

# Vérifie rapidement que le fichier existe
import os

if os.path.exists(path):
    print("📁 File OK")

    size = os.path.getsize(path)
    print("📦 Size:", size, "bytes")

else:
    print("❌ File missing")