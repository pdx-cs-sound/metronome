#!/usr/bin/python3
# Bart Massey

# Metronome

import pyaudio, struct, sys, time

# Sample rate in frames per second.
SAMPLE_RATE = 48_000

# Global sample clock. Updated by callback.
sample_clock = 0

# Next tick time in samples.
next_tick = 0

# Remaining tick duration, if any.
tick_timer = 0

# Tick length in samples.
tick_length = SAMPLE_RATE // 1000

# Tick interval in samples.
tick_interval = None

def callback(in_data, frames, time_info, status):
    global sample_clock, next_tick, tick_timer

    assert tick_interval is not None

    buffer = list()
    for i in range(frames):
        if next_tick == sample_clock:
            tick_timer = tick_length
            next_tick = sample_clock + tick_interval

        if tick_timer > 0:
            if tick_timer < tick_length // 2:
                buffer.append(1.0)
            else:
                buffer.append(-1.0)
            tick_timer -= 1
        else:
            buffer.append(0.0)
        sample_clock += 1
    return (struct.pack("{}f".format(frames), *buffer), pyaudio.paContinue)

# Set up the tick interval.
tick_interval = SAMPLE_RATE // (float(sys.argv[1]) / 60.0)

# Set up the stream.
pa = pyaudio.PyAudio()
stream = pa.open(rate = SAMPLE_RATE,
                 channels = 1,
                 format = pyaudio.paFloat32,
                 output = True,
                 frames_per_buffer = 128,
                 stream_callback = callback)
            

# Run the stream.
stream.start_stream()
while True:
    try:
        time.sleep(1)
    except:
        break
stream.stop_stream()
stream.close()
