## rosbag_recorder

ROS service to remotely start/stop recording selected topics to a named bag file.
Includes `*.srv` definitions necessary to issue requests.

## Building

 - Clone the repo into the `src` directory of your catkin workspace
 - Run `catkin_make` from the root of your catkin workspace
 - Run `catkin_make -DCMAKE_INSTALL_PREFIX=/opt/ros/<distro> install` or simply source `devel/setup.bash` from the root of your catkin workspace and copy `devel/include/rosbag_recorder` to the `include` folder of your ROS installation
 
## Running
### Start the service
- Start the service using rosrun: `rosrun rosbag_recorder rosbag_recorder_server.py`
- Start the service using launch file: `roslaunch rosbag_recorder rosbag_recorder.launch`
    - Pickle each bag after it's saved: `roslaunch rosbag_recorder rosbag_recorder.launch pickle:=true` _(Note, this could take a long time if you're saving super large amounts of data)_
- Use the `qml-ros-recorder` QML plugin in an application to start/stop recording remotely

### Start/Stop recording
Use a ROS service call to start and stop recording.
```python
import rosbag_recorder.srv as rbr

def start_saving(out_filename):
    rospy.wait_for_service('rosbag_recorder/record_topics')

    # Generate the topic list (robot and pressure controller topics)
    topic_list = []
    topic_list.extend(['/joint_states','/wrench','/tool_velocity'])
    topic_list.extend(['/pressure_control/echo','/pressure_control/pressure_data'])

    # Start saving data
    try:
        service = rospy.ServiceProxy('rosbag_recorder/record_topics', rbr.RecordTopics)
        response = service(out_filename, topic_list)
        return response.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def stop_saving(out_filename):
    # Stop saving data
    try:
        service = rospy.ServiceProxy('rosbag_recorder/stop_recording', rbr.StopRecording)
        response = service(out_filename)
        return response.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

```

### Graphing later
If you pickled your data after saving, you can use another set of scripts I made to plot them

[rosbag-pickle-graph](https://github.com/cbteeple/rosbag-pickle-graph)

`python graph_robot.py ft/up200_11162019_210947`
