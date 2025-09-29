# nofile – File to C/C++ Header Converter

This tool converts any binary file (`.bin`, `.png`, `.dat`, …)  
into C or C++ source/header files (`.h` + `.c` or `.h` + `.cpp`).

The generated output contains:
- **data array** (`const unsigned char[]`)
- **file size** (`size_t`)
- **SHA-256 hash** (as `const char[]`)
- auto-generated **include guard**
- comment with original file name and size

---

## Usage

```bash
python3 nofile.py -c   file1.bin file2.png
python3 nofile.py -c++ file1.bin file2.png
```

- `-c`   → output for C (`.c` + `.h`)  
- `-c++` → output for C++ (`.cpp` + `.h`)  

Each input file will generate two new files:  
- `<name>.h`  
- `<name>.c` or `<name>.cpp`  

Example:

```bash
python3 nofile.py -c logo.png
```

Generates:
- `logo_png.h`
- `logo_png.c`
