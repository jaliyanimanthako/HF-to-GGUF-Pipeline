import subprocess
import os
import shutil
from huggingface_hub import Repository, whoami, HfHubHTTPError


def push_gguf(repo_id: str, gguf_path: str, local_rsepo_dir: str = "./hf_tmp_repo"):
    # Check login
    try:
        whoami()
    except HfHubHTTPError:
        print("Not logged in. Prompting for login...")
        try:
            subprocess.run(["huggingface-cli", "login"], check=True)
        except subprocess.CalledProcessError as e:
            print("Login failed:", e)
            raise

    # Clone repo only if not already cloned
    if not os.path.isdir(os.path.join(local_repo_dir, ".git")):
        if os.path.exists(local_repo_dir):
            shutil.rmtree(local_repo_dir)
        repo = Repository(local_dir=local_repo_dir, clone_from=repo_id, use_auth_token=True)
    else:
        repo = Repository(local_dir=local_repo_dir)
        repo.git_pull()

    # Copy model file into the repo
    gguf_filename = os.path.basename(gguf_path)
    target_path = os.path.join(local_repo_dir, gguf_filename)
    shutil.copy(gguf_path, target_path)

    # Push to Hugging Face Hub
    repo.push_to_hub(commit_message=f"Upload {gguf_filename}")
    print(f"Successfully uploaded `{gguf_filename}` to `{repo_id}`")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Upload a GGUF model to Hugging Face Hub")
    parser.add_argument("--repo_id", required=True, help="Hugging Face repo ID (e.g. username/model-name)")
    parser.add_argument("--gguf_path", required=True, help="Path to .gguf file to upload")
    parser.add_argument("--local_repo_dir", default="./hf_tmp_repo", help="Path to local clone of the repo")
    args = parser.parse_args()

    push_gguf(
        repo_id=args.repo_id,
        gguf_path=args.gguf_path,
        local_repo_dir=args.local_repo_dir
    )


if __name__ == "__main__":
    main()
