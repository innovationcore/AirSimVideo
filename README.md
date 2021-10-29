# AirSimVideo
Manipulating an AirSim simulation remotely and extracting video

Proof-of-concept for manipulating drones in [AirSim](https://github.com/Microsoft/AirSim) and extracting images/videos during training. 

## Files
- settings.json - Settings for simulation. Copy to same directory as the AirSim binary, or to C:\Users\[username]\Documents\Airsim\settings.json
- connect.py - for testing connections to a headless remote sim
- training.py - demonstrates controlling a drone through the OpenAI Gym interface and getting images out. Saves a frame per-step. Frames can be stitched into a video using stitch_video.py.
- video_server.py - Connect to a training session and stream video to a local address. Can run at the same time as training.py.
