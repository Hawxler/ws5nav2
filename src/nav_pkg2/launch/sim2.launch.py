# 커스텀 2바퀴 차 + 커스텀 맵
import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ##########################
    # 1. 패키지 경로
    ##########################
    pkg_share = get_package_share_directory('nav_pkg2')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # URDF
    xacro_file = os.path.join(
        pkg_share,
        'description',
        'mobile_robot1.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command([
            'xacro ',
            xacro_file
        ]),

        value_type=str
    )

    # World
    world_file = os.path.join(
        pkg_share,
        'worlds',
        'simple_room.world'
    )

    # Gazebo 실행 + simple_room.world 실행
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_ros_share,
                'launch',
                'gazebo.launch.py'
            )
        ),

        launch_arguments={
            'world': world_file
        }.items()
    )

    ################################
    # Node: Robot State Publisher
    ################################
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ]
    )

    ################################
    # Node: Spawn Robot -> Gazebo에 mobile_robot1 생성
    ################################
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity',
            'mobile_robot1',

            '-topic',
            'robot_description',

            '-x',
            '0.0',

            '-y',
            '0.0',

            '-z',
            '0.03'
        ],

        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])