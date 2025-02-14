from picamera2 import Picamera2, Preview
from os import path
import time
from io import BytesIO
import json
import requests

picam2 = None
DELAY = 1

def trigger_camera(amount_of_pictures, vehicle_data, gcs_url):
    global picam2

    if picam2 is None:
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration()
        picam2.configure(camera_config)
        picam2.start_preview(Preview.NULL)
        picam2.start()
        time.sleep(1)
    else:
        picam2.start()

    for i in range(amount_of_pictures):
        start_time = time.time()
        current_time = take_and_send_picture_no_local(i, picam2, vehicle_data, gcs_url)
        time_elapsed_since_start = current_time - start_time
        delay_time = DELAY - time_elapsed_since_start
        if delay_time > 0:
            time.sleep(delay_time)
    picam2.stop()
    return {'message': 'Success!'}, 200

def take_and_send_picture_no_local(i, picam2, vehicle_data, gcs_url):
    '''
    Takes a picture and sends it back to the GCS. It does not save any images locally on the Raspberry Pi, and is used to prevent
    the SD card on the Raspberry Pi from filling and overloading the storage (and corrupting data).
    '''
    print('capturing image %i' % i)
    
    # Capture image into a BytesIO object
    image_stream = BytesIO()
    image = picam2.capture_image('main')
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)

    # Serialize vehicle data into a JSON string
    vehicle_data_json = json.dumps(vehicle_data)

    # Send image to GCS
    files = {
        'file': (f'000{i:02d}.jpg', image_stream, 'image/jpeg'),
    }
    headers = {}
    response = requests.request("POST", f"{gcs_url}/submit", headers=headers, files=files)

    # Send JSON to GCS
    json_stream = BytesIO(vehicle_data_json.encode('utf-8'))
    json_files = {
        'file': (f'000{i:02d}.json', json_stream, 'application/json'),
    }
    response = requests.request("POST", f"{gcs_url}/submit", headers=headers, files=json_files)

    return time.time()

def picture_locator(gcs_url):
    global picam2

    if picam2 is None:
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration()
        picam2.configure(camera_config)
        picam2.start_preview(Preview.NULL)
        picam2.start()
        time.sleep(1)
    else:
        picam2.start()

    try:
        image_stream = BytesIO()
        image = picam2.capture_image('main')
        image.save(image_stream, format='JPEG')
        image_stream.seek(0)

        image_file = {
            'file': (f'locator.jpg', image_stream, 'image/jpeg'),
        }

        headers = {}
        response = requests.request("POST", f"{gcs_url}/submit", headers=headers, files=image_file)
    except Exception as e:
        return {'message': 'Error. Could not capture and send image.'}, 400
    picam2.stop()
    return {'message': 'Success!'}, 200