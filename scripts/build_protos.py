import glob
import re
import subprocess
from pathlib import Path

"""
This script is used to compile the proto files into Python code
This can be executed from the root directory of the repo running
`uv run scripts/build_protos.py`
It will generate the files to `src/macrocosmos/generated/`
"""


def compile_protos():
    print("Setting up protobuf compiler...")

    root_dir = Path(__file__).parent.parent.absolute()

    package_name = "macrocosmos"
    compile_loc_name = "generated"
    proto_dir = root_dir / "protos"
    output_dir = root_dir / "src" / package_name / compile_loc_name
    compile_pkg_name = package_name + "." + compile_loc_name

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files for proper Python packaging
    Path(output_dir / "__init__.py").touch()

    # Ensure all subdirectories have __init__.py files
    for dir_path in output_dir.glob("**/*/"):
        Path(dir_path / "__init__.py").touch()

    # Find all .proto files
    print(f"Finding .proto files in {proto_dir}...")
    proto_files = glob.glob(str(proto_dir / "**" / "*.proto"), recursive=True)

    if not proto_files:
        print("No .proto files found!")
        return

    # Build the protoc command
    cmd = [
        "python",
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={output_dir}",
        f"--pyi_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        f"--protobuf-to-pydantic_out={output_dir}",
    ] + proto_files

    # Run the command
    print(f"Compiling {len(proto_files)} proto files...")
    subprocess.check_call(cmd)
    print("✅ Proto compilation complete!")

    # Fix imports in generated files (protoc uses relative imports)
    print("Fixing imports in generated files...")
    fix_imports(compile_pkg_name, output_dir)
    print("✅ Import fixes complete!")


def fix_imports(compile_pkg_name, output_dir):
    """Fix imports in all generated Python files recursively.

    e.g.
    Replace this: from apex.v1 import apex_pb2 as apex_dot_v1_dot_apex__pb2
    With this: from macrocosmos.generated.apex.v1 import apex_pb2 as apex_dot_v1_dot_apex__pb2
    """

    from_import_pattern = r"\nfrom ([\w.]+) import ([\w_]+_pb2)(?:\s+as\s+([\w_]+))?"
    import_pattern = r"\nimport ([\w.]+_pb2)(?:\s+as\s+([\w_]+))?"
    pattern_package_import = rf"({from_import_pattern})|({import_pattern})"

    def replace_package_import(match):
        # Extract all groups from the match
        groups = match.groups()

        if groups[0] is not None:
            # from import matched
            package_path = groups[1]
            module_name = groups[2]
            alias = groups[3]

            # Skip Google protobuf imports
            if package_path.startswith("google.protobuf"):
                return match.group(0)

            if alias:
                return f"from {compile_pkg_name}.{package_path} import {module_name} as {alias}"
            else:
                return f"from {compile_pkg_name}.{package_path} import {module_name}"

        # direct import matched
        full_import = groups[4]
        alias = groups[5]

        # Skip Google protobuf imports
        if full_import.startswith("google.protobuf"):
            return match.group(0)

        if alias:
            return f"import {compile_pkg_name}.{full_import} as {alias}"
        else:
            return f"import {compile_pkg_name}.{full_import}"

    for py_file in glob.glob(str(output_dir / "**/*.py"), recursive=True):
        with open(py_file, "r") as file:
            content = file.read()

        modified_content = re.sub(
            pattern_package_import, replace_package_import, content
        )

        if modified_content != content:
            with open(py_file, "w") as file:
                file.write(modified_content)


if __name__ == "__main__":
    compile_protos()
