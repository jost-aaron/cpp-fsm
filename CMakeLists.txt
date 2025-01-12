cmake_minimum_required(VERSION 3.0)

project(CPP_FSM)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

if(NOT DEFINED CPP_FSM_TARGETS)
    message(FATAL_ERROR "CPP_FSM_TARGETS variable must be set")
endif()

# Get a list of all state machine file names with cpp appeneded to it
string(REPLACE ".sm" ".cpp" CPP_FSM_SOURCES "${CPP_FSM_TARGETS}")
# Remove all path information from CPP_FSM_SOURCES
get_filename_component(CPP_FSM_SOURCES "${CPP_FSM_SOURCES}" NAME)
# Prepend the generated source directory to each file in CPP_FSM_SOURCES
list(TRANSFORM CPP_FSM_SOURCES PREPEND "${CMAKE_CURRENT_BINARY_DIR}/generated/src/")

# Call the python script that parses the state machine definitions. This runs at make time
add_custom_command(
    OUTPUT ${CPP_FSM_SOURCES} 
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generator.py ${CPP_FSM_TARGETS} 
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generator.py ${CPP_FSM_TARGETS}
    COMMENT "Running state machine parser"
)

add_library(cpp_fsm ${CPP_FSM_SOURCES})
target_include_directories(cpp_fsm PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/generated/include)

