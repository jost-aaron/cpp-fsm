cmake_minimum_required(VERSION 3.0)

project(StateMachineParser)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

add_custom_command(
    OUTPUT state_machine_output
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/state_machine_parser.py ${CMAKE_CURRENT_SOURCE_DIR}/state_machine_config.sm
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/state_machine_parser.py ${CMAKE_CURRENT_SOURCE_DIR}/state_machine_config.sm
    COMMENT "Running state machine parser"
)

add_custom_target(run_state_machine_parser ALL DEPENDS state_machine_output)

