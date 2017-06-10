from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, replace_in_file
import os


class NanaConan(ConanFile):
    name = "Nana"
    version = "1.5.1"
    license = "MIT"
    url = "https://github.com/jacmoe/conan-nana"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "png": [True, False], "jpeg": [True, False]}
    default_options = "shared=False", "png=True", "jpeg=True"
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
        png = "-DNANA_CMAKE_ENABLE_PNG:BOOL=ON" if self.options.png else ""
        jpeg = "-DNANA_CMAKE_ENABLE_JPEG:BOOL=ON" if self.options.jpeg else ""
        self.run('cmake nana %s %s %s %s' % (cmake.command_line, shared, png, jpeg))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*", dst="include", src="nana/include")
        self.copy("*nana.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["nana"]
        self.cpp_info.cppflags = ["-std=c++11"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("X11")
            self.cpp_info.libs.append("boost_system")
            self.cpp_info.libs.append("boost_filesystem")
            self.cpp_info.libs.append("boost_thread")
            self.cpp_info.libs.append("Xft")
            self.cpp_info.libs.append("fontconfig")
            self.cpp_info.libs.append("stdc++fs")
        if self.settings.os == "Linux" and self.options.png:
            self.cpp_info.libs.append("png")
        if self.settings.os == "Linux" and self.options.jpeg:
            self.cpp_info.libs.append("jpeg")
