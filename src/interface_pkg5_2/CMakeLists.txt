cmake_minimum_required(VERSION 3.8)
project(interface_pkg5_2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ==================================================
# 1. 기본 패키지
# ==================================================
# find dependencies
find_package(ament_cmake REQUIRED)
# ROS2 Interface 생성용
find_package(rosidl_default_generators REQUIRED)
# 나중에 custom msg/srv/action에서 사용할 가능성이 높은 메시지
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# =================================================
# 2. Custom Interface
# =================================================
# 아직 msg / srv / action 파일을 만들지 않았으므로
# 아래 부분은 일단 주석 처리한다.
#
# 인터페이스 파일을 만들면 활성화한다.

# rosidl_generate_interfaces(${PROJECT_NAME}
#     "msg/MyMessage1.msg"
#     "srv/MyService1.srv"
#     "action/MyAction1.action"

#     DEPENDENCIES
#     std_msgs
#     geometry_msgs
# )


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  set(ament_cmake_copyright_FOUND TRUE)

  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# ===========================================
# 3. Package
# ===========================================
ament_package()
