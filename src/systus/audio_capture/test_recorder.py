from systus.audio_capture.recorder import AudioRecorder

rec = AudioRecorder(device=0)

audio = rec.record(5)

if abs(audio).max() < 100:
    print("❌ Silence détecté")
else:
    print("✅ Audio OK")