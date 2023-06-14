find_package(SEAL)

add_library(sealpir pir.hpp pir.cpp pir_client.hpp pir_client.cpp pir_server.hpp
  pir_server.cpp)
target_link_libraries(sealpir SEAL::seal)

add_executable(main main.cpp)
add_executable(main2 main2.cpp)
target_link_libraries(main sealpir)
target_link_libraries(main2 sealpir)
