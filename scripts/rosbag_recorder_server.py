#!/usr/bin/env python

from rosbag_recorder.srv import *
import rospy
import psutil
import shutil
import subprocess
import signal
from os.path import expanduser
import os
import time

from bag_pickle import pickleBag

pidDict = {}
recording = False
pickle_on_complete = False

pb = pickleBag()
 
def recordTopics(req):
	global pidDict
	global recording

	if recording:
		pass

	command = "rosbag record -b 512 -O " + req.name
	print("Recording to bag named %s. Topics:"%(req.name))
	for t in req.topics:
		print(t)
		command += " " + t

	pidDict[req.name] = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, cwd="/tmp/")

	recording = True
	return RecordTopicsResponse(True)
 
def stopRecording(req, timeout = 2.0):
	global pidDict
	global recording
	global pb
	global pickle_on_complete

	if not recording:
		pass

	if req.name in pidDict:
		print("Stop recording to bag named %s"%(req.name))
		p = pidDict[req.name]
		process = psutil.Process(p.pid)
		children = process.children(recursive=True)
		for subProcess in children:
			subProcess.send_signal(signal.SIGINT)
		psutil.wait_procs(children, timeout=timeout)
		p.wait()

		# Pickle the bag after you're done saving
		time.sleep(0.5)
		if pickle_on_complete:
			pb.read_bag(req.name)
			pb.save_output()
			moveBag(req.name)


	else:
		print("No current recording with name %s!"%req.name)

	recording = False
	return StopRecordingResponse(True)


def moveBag(filename):
	base = os.path.dirname(filename)
	file = os.path.basename(filename)
	base_new = os.path.join(base,'bag')
	filename_new = os.path.join(base_new,file)

	if not os.path.exists(base_new):
            os.makedirs(base_new)

	shutil.move(filename, filename_new)

 
def rosbagRecorder():
	global pickle_on_complete
	rospy.init_node('rosbag_recorder_server')

	pickle_on_complete = rospy.get_param(rospy.get_name()+'/pickle_on_complete',False)
	print("PICKLE ON COMPLETE: %d"%(pickle_on_complete))

	recordServ = rospy.Service('record_topics', RecordTopics, recordTopics)
	stopServ = rospy.Service('stop_recording', StopRecording, stopRecording)
	print("Ready to record topics")
	rospy.spin()

if __name__ == "__main__":
	rosbagRecorder()
