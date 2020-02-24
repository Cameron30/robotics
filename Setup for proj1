# First run these to setup the file structure:

mkdir -p ~/catkin_ws/src

cd ~/catkin_ws/src

catkin_make

catkin_create_pkg proj1 std_msgs rospy roscpp

cd ..

catkin_make

. ~/catkin_ws/devel/setup.bash

# Now replace the proj1 folder with the proj1 git folder and then rebuild:

cd ~/catkin_ws

catkin_make

. ~/catkin_ws/devel/setup.bash

# Now you should be good to go. Nodes go into proj1/src, and need to be added to the proj1.launch file.

roslaunch proj1 proj1.launch
