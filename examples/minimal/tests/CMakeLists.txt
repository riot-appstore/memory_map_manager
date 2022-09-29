add_executable(test_0 minimal.c)
add_executable(test_1 minimal.cpp)

target_link_libraries(test_0 PUBLIC mmm_lib)
target_link_libraries(test_1 PUBLIC mmm_lib)

enable_testing()
add_test(NAME test_0 COMMAND test_0)
add_test(NAME test_1 COMMAND test_1)
