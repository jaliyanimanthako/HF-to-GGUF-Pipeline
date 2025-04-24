import argparse
import subprocess
import os
import shutil
from huggingface_hub import Repository, whoami, HfHubHTTPError

def main():
    parser = argparse.ArgumentParser(description="Upload a GGUF model to Hugging Face Hub")
    parser.add_argument("--repo_id", required=True, help="Hugging Face repo ID (e.g. username/model-name)")
    parser.add_argument("--gguf_path", required=True, help="Path to .gguf file to upload")
    parser.add_argument("--local_repo_dir", default="./hf_tmp_repo", help="Path to local clone of the repo")
    args = parser.parse_args()

    # Check login
    try:
        whoami()
    except HfHubHTTPError:
        print("Not logged in. Prompting for login...")
        try:
            subprocess.run(["huggingface-cli", "login"], check=True)
        except subprocess.CalledProcessError as e:
            print("Login failed:", e)
            return

    # Clone if not already cloned
    if not os.path.isdir(os.path.join(args.local_repo_dir, ".git")):
        if os.path.exists(args.local_repo_dir):
            shutil.rmtree(args.local_repo_dir)
        repo = Repository(local_dir=args.local_repo_dir, clone_from=args.repo_id, use_auth_token=True)
    else:
        repo = Repository(local_dir=args.local_repo_dir)
        repo.git_pull()

    # Copy model file into the repo
    gguf_filename = os.path.basename(args.gguf_path)
    target_path = os.path.join(args.local_repo_dir, gguf_filename)
    shutil.copy(args.gguf_path, target_path)

    # Push to Hub
    repo.push_to_hub(commit_message=f"Upload {gguf_filename}")
    print(f"Successfully uploaded {gguf_filename} to {args.repo_id}")

if __name__ == "__main__":
    main()
