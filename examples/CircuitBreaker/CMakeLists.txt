cmake_minimum_required(VERSION 3.10)

project(cpp_fsm_example
    VERSION 1.0
    DESCRIPTION "A C++ finite state machine example"
    LANGUAGES CXX)

# Minimum c++11 support for using cpp-fsm
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Specify a binary directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Find all state machine definitions and add cpp-fsm target
file(GLOB_RECURSE CPP_FSM_TARGETS "${CMAKE_CURRENT_SOURCE_DIR}/sm_defs/*.sm")
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../src/ cpp_fsm)
get_target_property(CPP_FSM_INCLUDES cpp-fsm INCLUDE_DIRECTORIES)

# Find all source files for this example 
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")
add_executable(cpp_fsm_example ${SOURCES})
add_dependencies(cpp_fsm_example cpp-fsm)
target_link_libraries(cpp_fsm_example PUBLIC cpp-fsm)
target_include_directories(cpp_fsm_example PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include ${CPP_FSM_INCLUDES})