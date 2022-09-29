/**
 ******************************************************************************
 * @addtogroup typedefs_mmm
 * @{
 * @file      mm_typedefs_type_1.h
 * @version   0.0.0
 *
 * @details   Generated from the memory map manager version 2.0.0
 ******************************************************************************
 */
#ifndef MM_TYPEDEFS_TYPE_1_H
#define MM_TYPEDEFS_TYPE_1_H

#ifdef __cplusplus
extern "C"
{
#endif

/* includes ******************************************************************/
#include <stdint.h>

#include "mm_cc.h"

/* tyepdefs ***************************************************************/
MM_PACKED_START
typedef union {
    struct {
        uint32_t record_1;
    };
    uint8_t data[4]; /**< Array for padding */
} type_1;
MM_PACKED_END

#ifdef __cplusplus
}
#endif

#endif /* MM_TYPEDEFS_TYPE_1_H */
/** @} **/