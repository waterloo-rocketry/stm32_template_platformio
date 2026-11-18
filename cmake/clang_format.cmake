# Format and check format using clang-format and rocketlib's .clang-format.

find_program(CLANG_FORMAT clang-format) # Resolves clang-format from PATH
set(clang_format_config ${CMAKE_CURRENT_SOURCE_DIR}/third_party/rocketlib/.clang-format)
if(CLANG_FORMAT)
	file(GLOB_RECURSE format_files CONFIGURE_DEPENDS src/*.c src/*.h inc/*.h)
	add_custom_target(format
		COMMAND ${CLANG_FORMAT} --style=file:${clang_format_config} -i ${format_files}
		COMMENT "Formatting sources with clang-format"
		VERBATIM
	)
	add_custom_target(format-check
		COMMAND ${CLANG_FORMAT} --style=file:${clang_format_config} --dry-run -Werror ${format_files}
		COMMENT "Checking formatting with clang-format"
		VERBATIM
	)
else()
	message(STATUS "clang-format not found, format targets disabled")
endif()
