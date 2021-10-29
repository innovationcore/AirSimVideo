import setup_path
import gym
import airgym
import airsim
import time
import cv2
import numpy as np

from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv, VecTransposeImage
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback

test_type = "drone"
ip="127.0.0.1"

video_length = 100
video_frames = []
video_folder = "videos"
image_folder = "images"

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
