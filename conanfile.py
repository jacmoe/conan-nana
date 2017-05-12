from conans import ConanFile, CMake, tools
import os


class NanaConan(ConanFile):
    name = "Nana"
    version = "1.5.1"
    license = "MIT"
    url = "https://github.com/jacmoe/conan-nana"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/cnjinhao/nana.git")
        self.run("cd nana && git checkout v1.5.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("nana/CMakeLists.txt", "project(nana)", '''project(nana)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake nana %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.*", dst="include", src="nana/include")
        self.copy("pop_ignore_diagnostic", dst="include", src="nana/include")
        self.copy("push_ignore_diagnostic", dst="include", src="nana/include")
        self.copy("*nana.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["nana"]
