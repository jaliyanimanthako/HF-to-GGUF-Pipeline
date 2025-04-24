import subprocess
import os
from llama_tools.venv import create_virtualenv

"""
This script automates the setup and build process for the `llama.cpp` project, a C++ implementation of Facebook's LLaMA models. It handles the cloning of the repository, initializing required git submodules, configuring the build environment using CMake with Ninja, compiling the project using a specified number of parallel jobs, and finally setting up a Python virtual environment with required dependencies.

Here's what each step does in detail:

1. **Argument Parsing**: Accepts a command-line argument `-j` or `--jobs`, which specifies the number of parallel jobs to use when building the project. This allows faster compilation using multiple CPU cores.

2. **Repository Cloning**: Checks if the `llama.cpp` directory already exists. If not, it clones the official GitHub repository to the local system using `git clone`.

3. **Submodule Initialization**: Ensures that all git submodules (dependencies within the repository) are initialized and updated using `git submodule update --init --recursive`.

4. **CMake Configuration**: Prepares the build environment using `cmake`. It specifies the use of Ninja as the build system and configures several options:
   - Build type is set to `Release` for optimized performance.
   - Tests are disabled (`LLAMA_BUILD_TESTS=OFF`) to speed up the build.
   - Examples and server components are enabled.
   - CURL support is disabled to avoid unnecessary dependencies.

5. **Project Build**: Compiles the code using the configured build settings and the number of parallel jobs specified by the user.

6. **Python Environment Setup**: Calls the `create_virtualenv` function from a custom `requirenments` module (assumed to be a local module), which creates a Python virtual environment and installs necessary dependencies for using Python bindings or utilities related to the project.

This script is useful for anyone who wants to quickly set up and build the `llama.cpp` project from source, especially in development or research environments where reproducibility and efficiency are important.
"""


def setup_llama(jobs: int = 4):
    repo_url = "https://github.com/ggerganov/llama.cpp.git"
    repo_dir = "llama.cpp"

    # Clone the repo if it doesn't exist
    if not os.path.exists(repo_dir):
        try:
            subprocess.run(["git", "clone", repo_url], check=True)
            print("Repository cloned.")
        except subprocess.CalledProcessError as e:
            print(f"Git clone failed: {e}")
            raise
    else:
        print("Repository already exists, skipping clone.")

    # Initialize submodules
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_dir, check=True)
        print("Submodules initialized.")
    except subprocess.CalledProcessError as e:
        print(f"Submodule update failed: {e}")
        raise

    # CMake configuration
    cmake_config_cmd = [
        "cmake",
        "-S", ".",
        "-B", "build",
        "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DLLAMA_BUILD_TESTS=OFF",
        "-DLLAMA_BUILD_EXAMPLES=ON",
        "-DLLAMA_BUILD_SERVER=ON",
        "-DLLAMA_CURL=OFF"
    ]

    try:
        subprocess.run(cmake_config_cmd, cwd=repo_dir, check=True)
        print("CMake configuration completed.")
    except subprocess.CalledProcessError as e:
        print(f"CMake config failed: {e}")
        raise

    # Build with -j X
    try:
        subprocess.run(["cmake", "--build", "build", "--config", "Release", f"-j{jobs}"], cwd=repo_dir, check=True)
        print(f"Build completed with -j{jobs}.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        raise

    # Create virtual environment and install requirements
    try:
        create_virtualenv()
        print("Virtual environment created and requirements installed.")
    except subprocess.CalledProcessError as e:
        print(f"Virtual environment setup failed: {e}")
        raise

    print("Setup completed successfully.")
    print("Run the following command to activate the virtual environment:")
    print(f"source ~/llama-cpp-venv/bin/activate")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Setup and build llama.cpp")
    parser.add_argument("-j", "--jobs", type=int, required=True, help="Number of parallel build jobs")
    args = parser.parse_args()
    setup_llama(jobs=args.jobs)


if __name__ == "__main__":
    main()
