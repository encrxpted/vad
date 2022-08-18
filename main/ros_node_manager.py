import rospy

from std_msgs.msg import Bool, Int8MultiArray

from audio_common_msgs.msg import AudioData


class ROSNodeManager:

	def __init__(self, callback):
		print('init ros node')
		rospy.init_node('vad', anonymous = True)
		self.start_listener(callback)
		self.start_publisher()
		#rospy.spin()

	def start_listener(self, callback):
		self.input = rospy.Subscriber('/audio/audio', AudioData, callback) 

	def start_publisher(self):
		self.publisher = rospy.Publisher('/voice_activity', Bool, queue_size=10)

	def publish(self, msg):
		self.publisher.publish(msg)

