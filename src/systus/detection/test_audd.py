from systus.detection.audd_client import AudDClient

client = AudDClient(
    api_token="a1f8dc29dd7765e68f96e90dc26b8cbc"
)

result = client.recognize_file("tests/audio/test.wav")

print("\n🎵 RESULT:")
print(result)