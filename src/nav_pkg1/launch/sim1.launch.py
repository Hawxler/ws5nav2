import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ===========================
    # 1. Package 경로
    # ===========================
    nav_pkg_share = get_package_share_directory('nav_pkg1')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # ===========================
    # 2. Xacro 파일 경로
    # ===========================
    xacro_file = os.path.join(
        nav_pkg_share,
        'description',
        'mobile_robot1.urdf.xacro'
    )

    # ===========================
    # 3. Gazebo World
    # ===========================
    world_file = os.path.join(
        nav_pkg_share,
        'worlds',
        'simple_room.world'
    )

    # ===========================
    # 4. Xacro -> URDF
    # ===========================
    robot_description = ParameterValue(
        Command([
            'xacro ',
            xacro_file
        ]),
        value_type=str
    )

    # ===========================
    # 5. Robot State Publisher
    # ===========================
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ]
    )

    # ===========================
    # 6. Gazebo 실행
    # ===========================
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

    # ===========================
    # 7. Gazebo에 로봇 Spawn
    # ===========================
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_mobile_rebot1',
        output='screen',
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
        ]
    )

    # ===========================
    # 8. RViz
    # ===========================
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[
            {
                'use_sim_time': True
            }
        ]
    )

    # ===========================
    # 9. Launch
    # ===========================
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        rviz,
    ])