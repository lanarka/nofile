
import sys, os
import hashlib

def to_c_identifier(name):
    return os.path.basename(name).replace(".", "_").replace("-", "_")

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

def generate_header(identifier, filename, size, hash_hex, cpp_mode):
    guard = identifier.upper() + "_H"
    cpp_begin = 'extern "C" {\n' if cpp_mode else ""
    cpp_end = '}\n' if cpp_mode else ""
    return f"""#ifndef {guard}
#define {guard}

/*
 * Generated from file: {filename}
 * Size: {size} bytes
 * SHA-256: {hash_hex}
 */

#include <stddef.h>

#ifdef __cplusplus
{cpp_begin}
#endif

extern const unsigned char {identifier}[];
extern const size_t {identifier}_len;
extern const char {identifier}_sha256[];

#define {identifier.upper()}_SIZE {size}

#ifdef __cplusplus
{cpp_end}
#endif

#endif /* {guard} */
"""

def generate_source(identifier, data, hash_hex):
    hex_lines = []
    for i in range(0, len(data), 12):
        chunk = data[i:i+12]
        line = ", ".join(f"0x{b:02X}" for b in chunk)
        hex_lines.append("    " + line)
    hex_text = ",\n".join(hex_lines)
    return f"""#include "{identifier}.h"

const unsigned char {identifier}[] = {{
{hex_text}
}};

const size_t {identifier}_len = sizeof({identifier});
const char {identifier}_sha256[] = "{hash_hex}";
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} -c|-c++ file1 [file2 ...]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "-c":
        cpp_mode = False
    elif mode == "-c++":
        cpp_mode = True
    else:
        print("Error: first argument must be -c or -c++")
        sys.exit(1)

    for filename in sys.argv[2:]:
        with open(filename, "rb") as f:
            data = f.read()

        identifier = to_c_identifier(filename)
        size = len(data)
        hash_hex = sha256_hex(data)

        h_name = identifier + ".h"
        c_name = identifier + (".cpp" if cpp_mode else ".c")

        with open(h_name, "w") as f:
            f.write(generate_header(identifier, filename, size, hash_hex, cpp_mode))

        with open(c_name, "w") as f:
            f.write(generate_source(identifier, data, hash_hex))

