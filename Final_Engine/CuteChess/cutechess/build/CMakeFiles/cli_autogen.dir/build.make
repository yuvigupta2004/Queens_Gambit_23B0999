# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build

# Utility rule file for cli_autogen.

# Include any custom commands dependencies for this target.
include CMakeFiles/cli_autogen.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/cli_autogen.dir/progress.make

CMakeFiles/cli_autogen:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC and UIC for target cli"
	/usr/bin/cmake -E cmake_autogen /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build/CMakeFiles/cli_autogen.dir/AutogenInfo.json RelWithDebInfo

cli_autogen: CMakeFiles/cli_autogen
cli_autogen: CMakeFiles/cli_autogen.dir/build.make
.PHONY : cli_autogen

# Rule to build all files generated by this target.
CMakeFiles/cli_autogen.dir/build: cli_autogen
.PHONY : CMakeFiles/cli_autogen.dir/build

CMakeFiles/cli_autogen.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cli_autogen.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cli_autogen.dir/clean

CMakeFiles/cli_autogen.dir/depend:
	cd /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build /home/yuvigupta/Queens_Gambit/Week_5/cpptest/CuteChess/cutechess/build/CMakeFiles/cli_autogen.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cli_autogen.dir/depend
