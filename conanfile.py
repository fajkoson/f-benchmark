from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class BpbookConan(ConanFile):
    name = "bpbook"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    requires = "nlohmann_json/3.10.5"
    build_requires = "ninja/1.10.2"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
