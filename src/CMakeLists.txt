cmake_minimum_required(VERSION 3.10)

project(CPP-FSM)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

if(NOT DEFINED CPP_FSM_TARGETS)
    message(FATAL_ERROR "CPP_FSM_TARGETS variable must be set")
endif()

## Get a list of all state machine file names with cpp appeneded to it
set(PROCESSED_SOURCES "")
foreach(SOURCE IN LISTS CPP_FSM_TARGETS)
    string(REPLACE ".sm" ".cpp" SOURCE_CPP "${SOURCE}")
    get_filename_component(SOURCE_CPP "${SOURCE_CPP}" NAME)
    list(APPEND PROCESSED_SOURCES "${CMAKE_CURRENT_BINARY_DIR}/generated/src/${SOURCE_CPP}")
endforeach()
set(CPP_FSM_SOURCES "${PROCESSED_SOURCES}")
message(STATUS "CPP_FSM_SOURCES processed: ${CPP_FSM_SOURCES}")


# Call the python script that parses the state machine definitions. This runs at make time
add_custom_command(
    OUTPUT ${CPP_FSM_SOURCES} 
    COMMAND PYTHONDONTWRITEBYTECODE=1 ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generator.py ${CPP_FSM_TARGETS} 
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generator.py ${CPP_FSM_TARGETS}
    COMMENT "Running state machine parser"
)
add_library(cpp-fsm ${CPP_FSM_SOURCES})
target_include_directories(cpp-fsm PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/generated/include)

