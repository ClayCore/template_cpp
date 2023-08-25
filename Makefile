.PHONY: build check clean docs format

TARGET_DIR := target

$(TARGET_DIR):
	mkdir -p $@

# Builds and compiles the project using the `meson.build` file
build: | $(TARGET_DIR)
	mkdir $(TARGET_DIR)
	meson $(TARGET_DIR)
	meson compile -C $(TARGET_DIR)

# Cleans the build directory.
clean: 
	rm -rf $(TARGET_DIR)

# Runs static analysis targets provided by the `meson.build` file.
check: | $(TARGET_DIR)
	meson compile clang-tidy -C $(TARGET_DIR)
	meson compile cppcheck -C $(TARGET_DIR)

# Generates documentation using `doxygen`
docs: | $(TARGET_DIR)
	meson compile docs -C $(TARGET_DIR)

# Formats all the files using `clang-format`
format: | $(TARGET_DIR)
	ninja -C $(TARGET_DIR) clang-format
