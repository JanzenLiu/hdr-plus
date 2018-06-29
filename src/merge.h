#ifndef HDRPLUS_MERGE_H_
#define HDRPLUS_MERGE_H_

#include "Halide.h"

// Fix@Jun-29 by Janzen:
//  1. Replace Halide::Image by Halide::Buffer

/*
 * merge -- fully merges aligned frames in the temporal and spatial
 * dimension to produce one denoised bayer frame.
 */
Halide::Func merge(Halide::Buffer<uint16_t> imgs, Halide::Func alignment);

#endif