
# cmd: python sort_ioc.py [input.ioc] [formatted_output.ioc]* 
# formatted_output.ioc is optional, if not provided, input.ioc will be overwritten


import sys

def sort_ioc_file(input_file, output_file=None):
    if output_file is None:
        output_file = input_file  # overwrite original by default

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filter out empty lines and strip whitespace
    lines = [line.rstrip() for line in lines if line.strip()]

    # Sort lines alphabetically by key (everything before '=')
    def key_func(line):
        if '=' in line:
            return line.split('=', 1)[0].strip()
        return line.strip()
    
    sorted_lines = sorted(lines, key=key_func)

    # Write back
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in sorted_lines:
            f.write(line + '\n')

    print(f"Sorted {input_file} -> {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sort_ioc.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    sort_ioc_file(input_file, output_file)
