from flask import Flask, request, jsonify
from collections import deque
import time

app = Flask(__name__)

data_stream = deque()  # Use a deque to store incoming data
window_size = 60  # Size of the time window for calculating moving average

@app.route('/data', methods=['POST'])
def receive_data():
    timestamp = time.time()
    value = float(request.json['value'])

    # Add data to the data stream
    data_stream.append((timestamp, value))

    # Remove data older than the window size
    while data_stream and data_stream[0][0] < timestamp - window_size:
        data_stream.popleft()

    return 'Data received successfully', 201

@app.route('/moving_average', methods=['GET'])
def get_moving_average():
    current_time = time.time()
    sum_values = 0
    count = 0

    # Calculate moving average for data within the window
    for timestamp, value in data_stream:
        if current_time - timestamp <= window_size:
            sum_values += value
            count += 1

    if count > 0:
        moving_avg = sum_values / count
    else:
        moving_avg = 0

    return jsonify({'moving_average': moving_avg})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
