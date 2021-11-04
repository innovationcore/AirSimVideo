import setup_path
import os
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

parser.add_argument('--ip', type=str, default="127.0.0.1")
parser.add_argument('--video_folder', type=str, default="videos")
parser.add_argument('--num_frames', type=int, default=100)
parser.add_argument('--image_folder', type=str, default="images")

args = parser.parse_args()

ip = args.ip

video_length = args.num_frames
video_frames = []
video_folder = args.video_folder
image_folder = args.image_folder

try:
    os.makedirs(image_folder)
    os.makedirs(video_folder)
except OSError:
    if not os.path.isdir(video_folder) or not os.path.isdir(image_folder):
        raise

env_type = "airgym:airsim-drone-sample-v0"
env1 = gym.make(
                env_type,
                ip_address=ip,
                step_length=0.25,
                image_shape=(84, 84, 1),
                vehicle_name="Drone1",
            )
env2 = gym.make(
                env_type,
                ip_address=ip,
                step_length=0.25,
                image_shape=(84, 84, 1),
                vehicle_name="Drone2",
            )

env1 = DummyVecEnv( [lambda: Monitor(env1)] )
env1 = VecTransposeImage(env1)
env1.reset()

env2 = DummyVecEnv( [lambda: Monitor(env2)] )
env2 = VecTransposeImage(env2)
env2.reset()

client1 = env1.get_attr("drone")[0]
client2 = env2.get_attr("drone")[0]
request = airsim.ImageRequest("cam", airsim.ImageType.Scene, False, False) # types are in airsim/types.py

response1 = client1.simGetImages([request])[0]  #type = airsim.ImageResponse
size1 = (response1.height, response1.width, 3) # Specified in write_png
response2 = client2.simGetImages([request])[0]  #type = airsim.ImageResponse

for i in range(video_length + 1):
    env1.step([env1.action_space.sample()])
    env2.step([env2.action_space.sample()])
    response1 = client1.simGetImages([request])[0]  #type = airsim.ImageResponse
    response2 = client2.simGetImages([request])[0]  #type = airsim.ImageResponse
    data1 = response1.image_data_uint8
    data1 = np.reshape(np.frombuffer(data1, dtype=np.uint8), size)
    data2 = response2.image_data_uint8
    data2 = np.reshape(np.frombuffer(data2, dtype=np.uint8), size)
    image_path1 = f"{image_folder}/Drone1_{env_type}_{i}.png"
    image_path2 = f"{image_folder}/Drone2_{env_type}_{i}.png"
    print(f"Writing: {image_path1}")
    airsim.utils.write_png(image_path1, data)
    print(f"Writing: {image_path2}")
    airsim.utils.write_png(image_path2, data)
env1.close()
env2.close()
