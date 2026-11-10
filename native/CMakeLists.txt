cmake_minimum_required(VERSION 3.20)
project(cortana_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module(cortana_native src/module.cpp)
