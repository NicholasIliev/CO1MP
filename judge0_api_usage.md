<h1>Usage</h1>
<h2>Exemplar Request</h2>

```json
{
    "source_code": "import math\nnum=input()\nprint(f'The square root of {num} is {math.sqrt(num)}')",
    "language_id": 71,
    "stdin": 16
}
```

<p> Would represent the Python (3.8.1) code:

```python
import math
num = input()
print(f'The square root of {num} is {math.sqrt()}')
```

---
<h2>HTTP Request Structure</h2>
The HTTP request is sent with the following parameters:

| # | Attribute | Type | Unit |  Description |  Default|
| :- | :----: | ---: | ---: | ---: | ------: |
| 1 | **source_code** | text |  | Program's source_code | NONE -  attribute **required** |
| 2 | **language_id** | integer |  | Language ID | NONE - attribute **required** |
| 3 | compiler_options | string (max 512 chars) |  | Compiler flags | ```null``` |
| 4 | command_line_arguments | string (max 512 chars) |  | Command line arguments | ```null``` |
| 5 | stdin | text |  | Input for program | ```null```. Program won't receive to standard input |
| 6 | expected_output | text |  | Expected output. Used to compare with stdout | ```null```. Program's stdout won't be compared |
| 7 | cpu_time_limit | float | second | Default runtime maximum | Depends on configuration |
| 8 | memory_limit | float | kilobyte | Limit address space of program | Depends on configuration |
| 9 | stack_limit | integer | kilobyte | Limit process stack | Depends on configuration |
| 10 | number_of_runs | integer |  | Run each program ```number_of_runs``` times and average | Depends on configuration |

---

<h2>Viable Language List</h2>
The full list of languages can be obtained from https://ce.judge0.com/languages/. The most popular can be summarised as:

| I.D. | Language |
| :---: | :------: |
| 45 | Assembly (NASM 2.14.02) |
| 46 | Bash (5.0.0) |
| 47 | Basic (FBC 1.07.1) |
| 48 | C (GCC 7.4.0) |
| 52 | C++ (GCC 7.4.0) |
| 49 | C (GCC 8.3.0) |
| 53 | C++ (GCC 8.3.0) |
| 50 | C (GCC 9.2.0) |
| 54 | C++ (GCC 9.2.0) |
| 51 | C# (Mono 6.6.0.161) |
| 55 | Common Lisp (SBCL 2.0.0) |
| 56 | D (DMD 2.089.1) |
| 57 | Elixir (1.9.4) |
| 58 | Erlang (OTP 22.2) |
| 44 | Executable |
| 59 | Fortran (GFortran 9.2.0) |
| 60 | Go (1.13.5) |
| 61 | Haskell (GHC 8.8.1) |
| 62 | Java (OpenJDK 13.0.1) |
| 63 | JavaScript (Node.js 12.14.0) |
| 64 | Lua (5.3.5) |
| 65 | OCaml (4.09.0) |
| 66 | Octave (5.1.0) |
| 67 | Pascal (FPC 3.0.4) |
| 68 | PHP (7.4.1) |
| 43 | Plain Text |
| 69 | Prolog (GNU Prolog 1.4.5) |
| 70 | Python (2.7.17) |
| 71 | Python (3.8.1) |
| 72 | Ruby (2.7.0) |
| 73 | Rust (1.40.0)y |
| 74 | TypeScript (3.7.4) |