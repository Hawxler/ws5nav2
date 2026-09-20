import math
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def make_pose(navigator, x, y, yaw=0.0):
    # x, y : 맵 좌표
    # yaw : 로봇이 도착해서 향할 방향 (rad)

    pose = PoseStamped()
    
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()

    # 위치
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0

    # yaw -> 쿼터니언
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(yaw/2.0)
    pose.pose.orientation.w = math.cos(yaw/2.0)

    return pose

def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    #1. 초기 위치
    # Gazebo spawn: x=0, y=0
    initial_pose = make_pose(
        navigator,
        0.0,
        0.0,
        0.0
    )
    navigator.setInitialPose(initial_pose)

    #2. Nav2 활성화 대기
    navigator.waitUntilNav2Active()

    #3. waypoints 작성
    '''
    point:
  x: 0.3784617483615875
  y: -1.5033303499221802
  z: -0.001434326171875
---
header:
  stamp:
    sec: 1789904128
    nanosec: 703617191
  frame_id: map
point:
  x: 1.4445329904556274
  y: -1.7789301872253418
  z: -0.001434326171875
---
header:
  stamp:
    sec: 1789904177
    nanosec: 743265688
  frame_id: map
point:
  x: 1.549721121788025
  y: -1.5608330965042114
  z: -0.001373291015625
---

    
    '''
    waypoints = [

        # waypoint 1
        make_pose(
            navigator,
            0.3,
            -1.5,
            0.0
        ),

        # waypoint 2
        make_pose(
            navigator,
            1.4,
            -1.7,
            math.pi / 2.0
        ),

        # waypoint 3
        make_pose(
            navigator,
            1.5,
            -1.5,
            math.pi
        ),

    ]

    # 4. Waypoint 실행
    navigator.followWaypoints(waypoints)

    # 5. 완료까지 대기
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback is not None:
            navigator.get_logger().info(
                'waypoint navigation running...'
            )

    # 6. 결과 확인
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info(
            "모든 Waypoint 이동 성공"
        )
        
    elif result == TaskResult.CANCELED:
        navigator.get_logger().warn(
            'Waypoint 이동 취소'
        )

    elif result == TaskResult.FAILED:
        navigator.get_logger().error(
            'Waypoint 이동 실패'
        )

    else:
        navigator.get_logger().warn(
            '알 수 없는 결과'
        )


    rclpy.shutdown()


if __name__ == '__main__':
    main()