import requests
from base64 import b64encode
import json

BASE_URL = 'http://127.0.0.1:5000/'


ENCODING = 'utf-8'
IMAGE_NAME = 'samples/sample.png'
JSON_NAME = 'output.json'

# first: reading the binary stuff
# note the 'rb' flag
# result: bytes
with open(IMAGE_NAME, 'rb') as open_file:
    byte_content = open_file.read()

# second: base64 encode read data
# result: bytes (again)
base64_bytes = b64encode(byte_content)

# third: decode these bytes to text
# result: string (in utf-8)
base64_string = base64_bytes.decode(ENCODING)

# optional: doing stuff with the data
# result here: some dict
raw_data = {'data': base64_string}

# now: encoding the data to json
# result: string
json_data = json.dumps(raw_data, indent=2)

# finally: writing the json string to disk
# note the 'w' flag, no 'b' needed as we deal with text here
# with open(JSON_NAME, 'w') as another_open_file:
#     another_open_file.write(json_data)

response = requests.post(BASE_URL + '/image', data=raw_data)
print(response)
