def synthesize(text):
    voice_url = f"https://voice.example.com/fake/{text[:12].strip()}.mp3"
    return {
        "audio_url": voice_url,
        "message": "Synthesized with neutral tone"
    }
