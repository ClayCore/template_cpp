#!/bin/sh

poetry run python src/build.py --root_path "../../." --deps "bgfx" "spdlog" "fmt" "glfw3"
