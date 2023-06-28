# WebSocket Stress Tester

This script is a WebSocket stress tester, designed to connect to a WebSocket server, send messages at a specified rate, and display stats regarding the number of messages sent and received.

## Installation

To run this script, you need Python 3.7 or higher. It is recommended to use a virtual environment to manage the dependencies. You can follow these steps to set up and activate a virtual environment:

1. Clone the project:
   ```
   git clone https://github.com/dwymark-celestron/web-socket-stress-test.git
   cd web-socket-stress-test
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```
   pip install websockets
   ```

## Usage

After setting up the virtual environment, you can run the script from the command line with various options:

```
python websocket_stress_test.py <url> [-c <connections>] [-m <messages>] [-ch <characters>]
```

The parameters are as follows:

- `<url>`: The URL of the WebSocket server to connect to.
- `-c <connections>` or `--connections <connections>`: The number of connections to open simultaneously (default: 1).
- `-m <messages>` or `--messages <messages>`: The number of messages to send per second (default: 1).
- `-ch <characters>` or `--characters <characters>`: The number of characters in each message (default: 10).

For example, if you want to stress test a WebSocket server at `ws://localhost:8000` with 5 connections, each sending 10 messages per second with 100 characters each, you would use:

```
python websocket_stress_test.py ws://localhost:8000 -c 5 -m 10 -ch 100
```

Press Ctrl+C to stop the test.

## Output

While running, the script will continuously output the total number of messages sent and received. If the WebSocket server closes the connection, the script will attempt to reopen the connection and continue the test. The script can also handle other errors such as invalid server URLs and invalid inputs.
