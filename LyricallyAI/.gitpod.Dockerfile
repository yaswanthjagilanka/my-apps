FROM gitpod/workspace-full
RUN sudo apt-get update && sudo apt-get install -y ffmpeg
RUN sudo apt install ffmpeg