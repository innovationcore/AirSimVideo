import setup_path
import airsim
import cv2
import numpy as np
import argparse 

parser = argparse.ArgumentParser(description='AirSim Test Connection')
parser.add_argument('--ip', type=str, default="127.0.0.1")
parser.add_argument('--vehicle_name', type=str, default="")
args = parser.parse_args()

client = airsim.MultirotorClient(ip=args.ip)
client.enableApiControl(True, vehicle_name=args.vehicle_name)
client.confirmConnection()
