# AirSimVideo
Manipulating an AirSim simulation remotely and extracting video

Proof-of-concept for manipulating drones in [AirSim](https://github.com/Microsoft/AirSim) and extracting images/videos during training. 

## Files
- settings.json - Settings for simulation. Copy to same directory as the AirSim binary, or to C:\Users\[username]\Documents\Airsim\settings.json
- connect.py - for testing connections to a headless remote sim
- training.py - demonstrates controlling a drone through the OpenAI Gym interface and getting images out. Saves a frame per-step. Frames can be stitched into a video using stitch_video.py.
- video_server.py - Connect to a training session and stream video to a local address. Can run at the same time as training.py.

## Steps
- Download one of the [AirSim releases](https://github.com/Microsoft/AirSim/releases), copy settings.json to the appropriate directory, and run the executable.
- (Optional) Test connection using connect.py.
- Create folders 'videos' and 'images' to save output. 
- Launch training.py to initialize an OpenAI Gym that makes random actions. Depending on your environment/goal you'll need to adjust the reward function in order to do meaningful training. This will save a frame after each action to 'images/', which can be stitched into a video using stitch_video.py. Not super useful, but demonstrates how to pull individual frames from the Agent.
- Launch video_server.py then go to http://localhost:5000/video_feed to monitor the training.
