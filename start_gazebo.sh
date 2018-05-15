
GZ_VERSION=$(gazebo --version | grep -Po "(?<=version )(\d)" | head -1)

source /usr/share/gazebo-${GZ_VERSION}/setup.sh
gazebo_assets=../aeroloop_gazebo
export GAZEBO_MODEL_PATH=${gazebo_assets}/models:${GAZEBO_MODEL_PATH}
export GAZEBO_RESOURCE_PATH=${gazebo_assets}/resources:${GAZEBO_RESOURCE_PATH}
export GAZEBO_PLUGIN_PATH=${gazebo_assets}/plugins:${GAZEBO_PLUGIN_PATH}
gazebo --verbose ${gazebo_assets}/worlds/betaloop_iris_arducopter_demo.world

