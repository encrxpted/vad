from read_wav import *
import time

PATH = "recording.wav"
AGGRESSIVENESS = 2

# Runs VAD on a wave file
# This worked!

def main():

    audio, sample_rate = read_wave(PATH)
    vad = webrtcvad.Vad(AGGRESSIVENESS)
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)

    #is_speech_dict = {} 	# maps timestamps to is speech
    #print("start")
    for frame in frames:
        #print("hello?")
        is_speech = vad.is_speech(frame.bytes, sample_rate)
    	print(is_speech)
    	#time.sleep(0.03)


if __name__ == '__main__':
    main()