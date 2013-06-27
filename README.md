py_re_comm
==========

A tool to directly communicate with RoboEarth backend without the django middleware.

Installation
===========

1. Edit re_connection.py
2. Edit UPLOAD_DIR to point to fuse mountpoint
3. Update SESAME_SERVER if it starts on another port (mostly you don't need to change this unless you have explicitly changed your settings)
4. Update SESAME_CONNECTOR_LIBS paths
5. Update DB_PATH (Make it point to roboearth's user.db file if you can)
6. Add py_re_comm to ROS_PACKAGE_PATH
7. rosmake re_srvs and re_msgs
8. Make sure Roboearth is running
8. Run roscore
9. Run re_comm.py
10. try running re_client.py to test if everything works
11. Read re_client.py for how to use other services

Usage
==========

1. Add py_re_comm to ROS_PACKAGE_PATH
2. Make sure Roboearth is running
3. Run roscore
4. Run re_comm.py
