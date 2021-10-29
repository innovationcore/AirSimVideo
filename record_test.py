import setup_path
import gym
import airgym
import airsim
import time
import cv2
import numpy as np
import argparse 

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv, VecTransposeImage

parser = argparse.ArgumentParser(description='AirSim Test Launcher')

parser.add_argument('--test_type', type=str, default="drone")
parser.add_argument('--ip', type=str, default="127.0.0.1")
parser.add_argument('--video_folder', type=str, default="videos")
parser.add_argument('--num_frames', type=int, default=100)
parser.add_argument('--image_folder', type=str, default="images")

args = parser.parse_args()

test_type = args.test_type
ip = args.ip

video_length = args.num_frames
video_frames = []
video_folder = args.video_folder
image_folder = args.image_folder

if test_type == "drone":
    env_type = "airgym:airsim-drone-sample-v0"
    env = gym.make(
                    env_type,
                    ip_address=ip,
                    step_length=0.25,
                    image_shape=(84, 84, 1),
                )
else:
    env_type = "airgym:airsim-car-sample-v0"
    env = gym.make(
                    env_type,
                    ip_address=ip,
                    image_shape=(84, 84, 1),
                )

env = DummyVecEnv( [lambda: Monitor(env)] )
env = VecTransposeImage(env)
env.reset()

client = env.get_attr("drone")[0]
request = airsim.ImageRequest("cam", airsim.ImageType.Scene, False, False) # types are in airsim/types.py

response = client.simGetImages([request])[0]  #type = airsim.ImageResponse
size = (response.height, response.width, 3) # Specified in write_png

for i in range(video_length + 1):
    env.step([env.action_space.sample()])
    response = client.simGetImages([request])[0]  #type = airsim.ImageResponse
    data = response.image_data_uint8
    data = np.reshape(np.frombuffer(data, dtype=np.uint8), size)
    image_path = f"{image_folder}/{env_type}_{i}.png"
    print(f"Writing: {image_path}")
    airsim.utils.write_png(image_path, data)
env.close()



"""
 Example of building a video from these frames. 

 Capturing individual frames is helpful for debugging. This could be moved to
 the main loop, but would require some more futzing with the data before passing
 it to VideoWriter
"""   
filenames = sorted(glob.glob(image_folder+"/*.png"))
for filename in filenames:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    video_frames.append(img)

out = cv2.VideoWriter(video_folder + "/drone_video.mp4", cv2.VideoWriter_fourcc(*'MP4V'), 15, size)
for frame in video_frames:
    out.write(frame)
out.release()
