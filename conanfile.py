from conans import ConanFile, CMake, tools


class ConandbusasioConan(ConanFile):
    name = "dbus-asio"
    version = "0.1"
    license = "LGP-3.0"
    description = "Conan package for the dbus-asio library."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    requires = "boost/1.71.0"


    def source(self):
        self.run("git clone https://github.com/dbus-asio/dbus-asio.git")
        tools.replace_in_file("dbus-asio/CMakeLists.txt", "project(dbus-asio VERSION 1.0.0)",
                              '''project(dbus-asio VERSION 1.0.0)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        tools.replace_in_file("dbus-asio/CMakeLists.txt", '''install(TARGETS dbus-asio
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
	PUBLIC_HEADER DESTINATION include/libdbus-asio)

install(FILES ${CMAKE_BINARY_DIR}/dbus-asio.pc
	DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)

install(FILES dbus-asio-config.cmake
	DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/dbus-asio/)''',"")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="dbus-asio")
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses")
        self.copy("*.h", dst="include", src="dbus-asio/src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["dbus-asio"]

