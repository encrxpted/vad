from read_wav import *
import time

PATH = "recording.wav"
AGGRESSIVENESS = 2

def main():

    audio, sample_rate = read_wave(PATH)
    vad = webrtcvad.Vad(AGGRESSIVENESS)
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)

    #is_speech_dict = {} 	# maps timestamps to is speech
    #print("start")
    count = 0
    for frame in frames:
        #print("hello?")
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        #print(len.bytes))
        #if count == 10:
        print(frame.bytes)
            #print("\n")
            #print(len(frame.bytes))
        count = count + 1
    	#print(is_speech)
    	#print("\n")
    	#time.sleep(0.03)


if __name__ == '__main__':
    main()