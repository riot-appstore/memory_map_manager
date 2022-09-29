
add_library(mmm_lib
  mm_cc.h
  mm_meta.h
  mm_typedefs_map_1.h
  mm_typedefs_type_1.h
  mm_typedefs.h
)

target_include_directories(mmm_lib PUBLIC .)
set_target_properties(mmm_lib PROPERTIES LINKER_LANGUAGE CXX)
