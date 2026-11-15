cmake_minimum_required(VERSION 3.22)

# Set the project name
set(CMAKE_PROJECT_NAME stm32h5_template)

# Setup compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

# Define the build type
if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE "Release")
endif()

# Enable compile command to ease indexing with e.g. clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

# Core project settings
project(${CMAKE_PROJECT_NAME})
message("Build type: " ${CMAKE_BUILD_TYPE})

# Enable CMake support for ASM and C languages
enable_language(C ASM)

# Create an executable object type
add_executable(${CMAKE_PROJECT_NAME})

add_subdirectory(third_party/stm32cubemx/cmake/stm32cubemx)
add_subdirectory(third_party/rocketlib)

# Link directories setup
target_link_directories(${CMAKE_PROJECT_NAME} PRIVATE
	# Add user defined library search paths
)

# Source files to include in build

set(source_dir src)
# Recursively add all sources (.c files) in src/
file(GLOB_RECURSE sources CONFIGURE_DEPENDS ${source_dir}/*.c)
# Add source files in src/ which should be excluded from build into exclude_sources:
# Note GLOB_RECURSE returns absolute paths so our exclude_sources must also be absolute paths,
#	hence use CMAKE_CURRENT_SOURCE_DIR when manually excluding sources.
# file(GLOB_RECURSE exclude_sources CONFIGURE_DEPENDS ${source_dir}/exclude_sources/*.c)
# list(APPEND exclude_sources
# 	${CMAKE_CURRENT_SOURCE_DIR}/src/exclude_file1.c
# 	${CMAKE_CURRENT_SOURCE_DIR}/src/exclude_file2.c
# )
# list(REMOVE_ITEM sources ${exclude_sources})
target_sources(${CMAKE_PROJECT_NAME} PRIVATE ${sources})

# Add include paths
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE inc)

# Add project symbols (macros)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
	# Set BOARD_TYPE_UNIQUE_ID and BOARD_INST_UNIQUE_ID, e.g.:
	# BOARD_TYPE_UNIQUE_ID=BOARD_TYPE_ID_INJECTOR
	# BOARD_INST_UNIQUE_ID=BOARD_INST_ID_ROCKET
)

# Remove wrong libob.a library dependency when using cpp files
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)
 
# Add linked libraries
target_link_libraries(${CMAKE_PROJECT_NAME}
	stm32cubemx

	# Add rocketlib sources
	rocketlib::can_message
)

# Add flash target
add_custom_target(flash
	COMMAND STM32_Programmer_CLI -c port=SWD -w $<TARGET_FILE:${CMAKE_PROJECT_NAME}> -v -rst
	DEPENDS ${CMAKE_PROJECT_NAME}
	USES_TERMINAL
)
