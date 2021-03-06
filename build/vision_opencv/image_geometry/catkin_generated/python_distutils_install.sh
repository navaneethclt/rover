#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/rover/catkin_ws_backup/src/vision_opencv/image_geometry"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/rover/catkin_ws_backup/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/rover/catkin_ws_backup/install/lib/python2.7/dist-packages:/home/rover/catkin_ws_backup/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/rover/catkin_ws_backup/build" \
    "/usr/bin/python2" \
    "/home/rover/catkin_ws_backup/src/vision_opencv/image_geometry/setup.py" \
    egg_info --egg-base /home/rover/catkin_ws_backup/build/vision_opencv/image_geometry \
    build --build-base "/home/rover/catkin_ws_backup/build/vision_opencv/image_geometry" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/rover/catkin_ws_backup/install" --install-scripts="/home/rover/catkin_ws_backup/install/bin"
