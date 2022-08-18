from ros_node_manager import ROSNodeManager
import rospy
import _thread as thread
import numpy as np
import torch
torch.set_num_threads(1)
import torchaudio
torchaudio.set_audio_backend("soundfile")

class Main:

	def __init__(self):
		def ros_spin():
			rospy.spin()
		self.loaded = False
		self.count = 0
		self.last_audio_data = []

		self.ros_node = ROSNodeManager(self.callback)
		thread.start_new_thread(ros_spin,())

		self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)
		print("Got model")
		self.loaded = True

	def callback(self, audio_chunk):
		if self.loaded and self.count % 3 == 2:
			new_audio_data = list(audio_chunk.data)
			self.last_audio_data.extend(new_audio_data)
			#print(len(bytes(self.last_audio_data)))
			#audio_int16 = np.frombuffer(bytes(self.last_audio_data), np.int16)
			audio_float32 = self.int2float(np.array(self.last_audio_data))
			new_confidence = self.model(torch.from_numpy(audio_float32), 16000).item()
			print(new_confidence)
		elif self.loaded and self.count % 3 == 0:
			self.last_audio_data = list(audio_chunk.data)
		else:
			self.last_audio_data.extend(list(audio_chunk.data))

		self.count += 1

	def int2float(self, sound):
		abs_max = np.abs(sound).max()
		sound = sound.astype('float32')
		if abs_max > 0:
			sound *= 1/abs_max
		sound = sound.squeeze()  # depends on the use case
		return sound

def main():
	m = Main()
	while not rospy.is_shutdown():
		pass

if __name__ == '__main__':
    main()

