# Copyright (c) Alibaba Cloud.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
from argparse import ArgumentParser
from src.gradio_ui import create_demo

REVISION = 'v1.0.4'


def get_args():
    """
    Parses command-line arguments for the application.
    """
    parser = ArgumentParser()
    parser.add_argument("--revision", type=str, default=REVISION)
    parser.add_argument("--cpu-only", action="store_true", help="Run demo with CPU only (currently no-op)")

    # Arguments for OLLAMA configuration
    parser.add_argument("--ollama-model", type=str, default="qwen2.5vl:32b",
                        help="The name of the multi-modal model to use with OLLAMA (e.g., 'llava', 'llava:13b').")
    parser.add_argument("--ollama-host", type=str, default="http://192.168.235.62:11434",
                        help="The host address for the OLLAMA server.")

    # Arguments for Gradio server
    parser.add_argument("--share", action="store_true", default=False,
                        help="Create a publicly shareable link for the interface.")
    parser.add_argument("--inbrowser", action="store_true", default=False,
                        help="Automatically launch the interface in a new tab on the default browser.")
    parser.add_argument("--server-port", type=int, default=7860,
                        help="Demo server port.")
    parser.add_argument("--server-name", type=str, default="127.0.0.1",
                        help="Demo server name.")

    args = parser.parse_args()
    return args


def launch_demo(args):
    """
    Launches the Gradio demo interface.
    """
    # Set Gradio temp directory if specified by environment variable
    uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR")
    if uploaded_file_dir:
        print(f"Setting Gradio temp directory to: {uploaded_file_dir}")
        os.makedirs(uploaded_file_dir, exist_ok=True)

    demo = create_demo(args)
    
    print("Launching Gradio demo...")
    demo.queue().launch(
        share=args.share,
        inbrowser=args.inbrowser,
        server_port=args.server_port,
        server_name=args.server_name,
    )


def main():
    """
    Main function to run the application.
    """
    args = get_args()
    launch_demo(args)


if __name__ == '__main__':
    main()