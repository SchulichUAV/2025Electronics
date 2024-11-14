# Buit to sync with GCS2025 in Schulich UAV repository/organization
# Built for Raspberry Pi 5 (Linux OS)

from picamera2 import Picamera2, Preview
from flask import Flask, jsonify, request
from flask_cors import CORS
from math import ceil
import requests
import threading
import socket
import json
import sys
import time
from io import BytesIO
from os import path
import argparse
import RPi.GPIO as GPIO

GCS_URL = "http://192.168.1.65:80"
VEHICLE_PORT = "udp:127.0.0.1:5006"
ALTITUDE = 25
UDP_PORT = 5005

picam2 = None
vehicle_connection = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins" : "*"}}) # Overriding CORS for external access


