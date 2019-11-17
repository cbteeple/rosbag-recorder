import rosbag
import pickle
import sys
from rospy_message_converter import message_converter

class pickleBag:
	def __init__(self):
		pass

	'''
	Read in the bag file and convert it to a useful dictionary
	'''
	def read_bag(self,filename):
		self.filename=filename.strip('\n')
		print(' ')
		print('Pickling "%s"'%(self.filename))

		bag = rosbag.Bag(self.filename)

		time_offset = 0
		self.out = dict()
		for idx, (topic, msg, mt) in enumerate(bag.read_messages()):
			new_line = dict()
			new_line['msg'] = message_converter.convert_ros_message_to_dictionary(msg)	

			if idx is 0:
				time_offset = float(mt.to_sec())
				new_line['timestamp'] = 0
			else:
				new_line['timestamp']  = float(mt.to_sec()-time_offset)

			#print(new_line)
			topic = topic[1:]
			topic = topic.replace("/","_")

			if not self.out.get(topic):
				self.out[topic]=[]

			self.out[topic].append(new_line)

		bag.close()


	'''
	Pickle the dictionary for further use in python data processing
	'''
	def save_output(self, out_filename=None):
		if not out_filename:
			out_filename = self.filename.replace('.bag','.pkl')

		with open(out_filename,'w+') as f:
			pickle.dump(self.out,f)
			f.close()

		print('Pickling Successful!')


if __name__ == '__main__':
	if len(sys.argv)==2:
		pb=pickleBag()
		pb.read_bag(str(sys.argv[1]))
		pb.save_output()
	elif len(sys.argv)==3:
		pb=pickleBag()
		pb.read_bag(str(sys.argv[1]))
		pb.save_output(str(sys.argv[2]))
	else:
		print('Usage:')
		print('python convert_bag [BAG NAME]')
		print('python convert_bag [BAG NAME] [OUTPUT NAME]')
