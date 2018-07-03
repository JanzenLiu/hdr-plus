// basic raw image loader for Halide::Buffer<T> or other image with same API
// code largely appropriated from halide_image_io.h

// Fix@Jun-29 by Janzen:
//  1. Replace directly passed format and arguments to by a char* with value copied

#ifndef HALIDE_LOAD_RAW_H
#define HALIDE_LOAD_RAW_H

#include "Halide.h"
#include "halide_image_io.h"
#include <stdio.h>


namespace Halide {
namespace Tools {

namespace Internal {

struct PipeOpener {
    PipeOpener(const char* cmd, const char* mode) : f(popen(cmd, mode)) {
        // nothing
    }
    ~PipeOpener() {
        if (f != nullptr) {
            pclose(f);
        }
    }
    // read a line of data skipping lines that begin with '#"
    char *readLine(char *buf, int maxlen) {
        char *status;
        do {
            status = fgets(buf, maxlen, f);
        } while(status && buf[0] == '#');
        return(status);
    }
    FILE * const f;
};

} // namespace Internal

inline bool is_little_endian() {
    int value = 1;
    return ((char *) &value)[0] == 1;
}

inline void swap_endian_16(uint16_t &value) {
    value = ((value & 0xff)<<8)|((value & 0xff00)>>8);
}


/**
 * Load a given raw image file into memory.
 *
 * @param filename      Path of the raw image to load
 * @param data          uint16_t pointer to hold the loaded image
 * @param width         Width of the image
 * @param height        Height of the image
 * @return              true on success, false on failure
 */
template<Internal::CheckFunc check = Internal::CheckFail>
bool load_raw(const std::string &filename, uint16_t* data, int width, int height) {
    char out[1000];  // to store output
    int ret;  // to store string formatting result

    // -c Write image data to standard output
    // -D Document mode without scaling (totally raw)
    // -6 Write 16-bit instead of 8-bit
    // -W Don't automatically brighten the image
    // -g -g <p ts> Set custom gamma curve (default = 2.222 4.5)
    Internal::PipeOpener f(("../tools/dcraw -c -D -6 -W -g 1 1 " + filename).c_str(), "r");
    ret = sprintf(out, "File %s could not be opened for reading\n", filename.c_str());
    if (!check(f.f != nullptr, out)) return false;

    int in_width, in_height, maxval;
    char header[256];
    char buf[1024];
    bool fmt_binary = false;

    // ==========================
    // Read and Check File Header
    // ==========================
    f.readLine(buf, 1024);
    if (!check(sscanf(buf, "%255s", header) == 1, "Could not read PGM header\n")) return false;
    if (header == std::string("P5") || header == std::string("p5")) fmt_binary = true;
    if (!check(fmt_binary, "Input is not binary PGM\n")) return false;

    // =====================
    // Read Width and Height
    // =====================
    f.readLine(buf, 1024);
    if (!check(sscanf(buf, "%d %d\n", &in_width, &in_height) == 2, "Could not read PGM width and height\n")) return false;

    // ===========
    // Check Width
    // ===========
    ret = sprintf(out, "Input image '%s' has width %d, but must must have width of %d\n", filename.c_str(), in_width, width);
    if (!check(in_width == width, out)) return false;

    // ============
    // Check Height
    // ============
    ret = sprintf(out, "Input image '%s' has height %d, but must must have height of %d\n", filename.c_str(), in_height, height);
    if (!check(in_height == height, out)) return false;

    // ===========================
    // Read Bit Depth of the image
    // ===========================
    f.readLine(buf, 1024);
    if (!check(sscanf(buf, "%d", &maxval) == 1, "Could not read PGM max value\n")) return false;

    // ===============
    // Check Bit Depth
    // ===============
    if (!check(maxval == 65535, "Invalid bit depth (not 16 bits) in PGM\n")) return false;

    // ===============
    // Read Image Data
    // ===============
    if (!check(fread((void *) data, sizeof(uint16_t), width*height, f.f) == (size_t) (width*height), "Could not read PGM 16-bit data\n")) return false;

    if (is_little_endian()) {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                swap_endian_16(data[y * width + x]);
            }
        }
    }

    return true;
}

} // namespace Tools
} // namespace Halide

#endif