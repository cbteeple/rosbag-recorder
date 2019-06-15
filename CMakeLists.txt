cmake_minimum_required(VERSION 2.8.3)
project(rosbag_recorder)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_service_files(
  FILES
  RecordTopics.srv
  StopRecording.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
)
