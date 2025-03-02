#!/usr/bin/env python3
"""
Run script for the Streamlit application.
This script launches the Streamlit app defined by the provided app path,
allowing additional command-line arguments to be forwarded to Streamlit.

python run.py --app-path src/app/main.py -- --server.port 8502
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path
import shutil

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Launch the Streamlit application with optional arguments."
    )
    parser.add_argument(
        "--app-path",
        type=Path,
        default=Path("src/app/main.py"),
        help="Path to the Streamlit application (default: src/app/main.py)"
    )
    parser.add_argument(
        "streamlit_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to the Streamlit command."
    )
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()

    app_path = args.app_path.resolve()
    if not app_path.exists():
        logging.error("Could not find the Streamlit app at %s", app_path)
        sys.exit(1)

    # Check if 'streamlit' is available in PATH
    if shutil.which("streamlit") is None:
        logging.error("Streamlit is not installed or not found in your PATH. Please install it with 'pip install streamlit'.")
        sys.exit(1)

    command = ["streamlit", "run", str(app_path)] + args.streamlit_args
    logging.info("Running command: %s", " ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Streamlit exited with a non-zero exit code: %s", e)
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

