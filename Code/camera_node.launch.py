# team7project2

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import yaml

PACKAGE_NAME = 'ucsd_robocar_sensor2_pkg'
FILE_CONFIG_NAME = 'camera_node.yaml'
def generate_launch_description():
    # # Optional: Get config directory
    # config_dir = os.path.dir(get_package_share_directory(PACKAGE_NAME), 'config')
    # # Create the launch configuration variables
    # config = os.path.join(config_dir, FILE_CONFIG_NAME)
    # with open(config,'r') as f:
    #     params = yaml.safe_load(f)['camera_node']['ros__parameters']
    #     """
    #     camera_node:
    #         ros_parameters:
    #             x: 5
    #     """

    ld = LaunchDescription()

    camera_node = Node(
        package=PACKAGE_NAME,
        executable='camera_node',
        name='camera_node',
        output='screen'
    )

    ld.add_action(camera_node)

    return ld