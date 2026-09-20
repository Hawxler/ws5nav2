# RViz의 "Nav2 Goal" 버튼을 대체하여 목적지를 지정하는 코드
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator

def make_pose(navigator, x, y, yaw_z=0.0, yaw_w=1.0):
    pose = PoseStamped()

    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0

    pose.pose.orientation.z = yaw_z
    pose.pose.orientation.w = yaw_w

    return pose

def main():
    rclpy.init()

    navigator = BasicNavigator()

    # 1. 초기 위치
    # Gazebo spawn 위치 (0, 0)을 사용
    initial_pose = make_pose(
        navigator,
        0.0,
        0.0
    )

    navigator.setInitialPose(initial_pose)

    # 2. Nav2 확성화 대기
    navigator.waitUntilNav2Active()

    # 3. 목표 위치
    goal_pose = make_pose(
        navigator,
        1.0,
        -1.0
    )

    # 4. 자율주행 시작
    navigator.goToPose(goal_pose)

    # 5. 이동 완료 대기
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()

        if feedback:
            navigator.get_logger().info('Navigation running...')
    
    # 6. 결과
    result = navigator.getResult()
    navigator.get_logger().info(f'네비게이션 종료: {result}')

    rclpy.shutdown()

if __name__=='__main__':
    main()