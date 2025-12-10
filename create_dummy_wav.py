import wave
import struct
import math

# Output file path
output_path = "dummy.wav"

# WAV file settings
duration_seconds = 1.5      # short beep sound
sample_rate = 16000
frequency = 440             # A4 tone
volume = 0.5

num_samples = int(sample_rate * duration_seconds)

with wave.open(output_path, "w") as wav_file:
    wav_file.setnchannels(1)          # mono
    wav_file.setsampwidth(2)          # 16-bit audio
    wav_file.setframerate(sample_rate)

    for i in range(num_samples):
        sample = volume * math.sin(2 * math.pi * frequency * (i / sample_rate))
        wav_file.writeframes(struct.pack("<h", int(sample * 32767)))

print(f"dummy.wav created successfully: {output_path}")
