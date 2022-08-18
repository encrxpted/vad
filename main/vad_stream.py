from ros_node_manager import ROSNodeManager
import webrtcvad
import rospy
import numpy as np
import _thread as thread

AGGRESSIVENESS = 2
SAMPLE_RATE = 16000

# Attempt at doing VAD on stream
# Issue: Frame size is wrong, don't know how to convert

class Main:

	def __init__(self):
		def ros_spin():
			rospy.spin()

		self.audio = []	# List of bytes to process
		self.vad = webrtcvad.Vad(AGGRESSIVENESS)
		self.ros_node = ROSNodeManager(self.callback)
		thread.start_new_thread(ros_spin,())
		self.count = 0

	def callback(self, input):
		frame = (list(input.data)) 	# data is bytes object
		#if self.count == 0:
		#print("input: ")
		#print(input.data)
		#print(len(input.data))
		#print(len(frame))
		self.audio.extend(frame)
		#self.count += 1

def main():
	m = Main()
	#print("here?")
	offset = 0
	while not rospy.is_shutdown():
		#b = np.array(m.audio)

		#if len(b) >= offset + 120:
		if len(m.audio) >= offset + 960:
			#print("processing frame")
			a = m.audio[offset:offset + 960] 	# grab elements for correct frame size
			#print("numpy arr a:"+ str(len(a)))
			#print(bytearray(a))
			#print(a)
			#print("frame: " + str(len(frame)))
			#print("bytes:")
			#print((bytes(a)))
			is_speech = m.vad.is_speech(bytes(a), SAMPLE_RATE)
			m.ros_node.publish(is_speech)
			print(is_speech)

			# numpy conversion worked but it is grief because it padded 0s???
			offset += 960

if __name__ == '__main__':
    main()
