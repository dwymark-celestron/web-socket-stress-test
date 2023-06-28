import asyncio
import websockets
import signal
import argparse

# Global variables
total_messages_sent = 0

# Handle Ctrl+C
def signal_handler(sig, frame):
    print("\nTest stopped by user")
    asyncio.get_event_loop().stop()

# Function to display stats
async def display_stats():
    while True:
        print(f"Total messages sent: {total_messages_sent}")
        await asyncio.sleep(1)

# Function to send messages
async def send_messages(url, messages_per_second, characters_per_message):
    global total_messages_sent

    websocket = await websockets.connect(url)

    try:
        while True:
            try:
                await websocket.send("x" * characters_per_message)
                total_messages_sent += 1
                await asyncio.sleep(1 / messages_per_second)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed, error code: {e.code}, reason: {e.reason}")
                print("Reopening connection...")
                websocket = await websockets.connect(url)
            except asyncio.CancelledError:
                break
    finally:
        print("Exiting send_messages")
        await websocket.close()

# Main function
async def main(url, num_connections, messages_per_second, characters_per_message):
    print("Press Ctrl+C to stop the test")

    tasks = [asyncio.ensure_future(send_messages(url, messages_per_second, characters_per_message)) for _ in range(num_connections)]

    stats_task = asyncio.ensure_future(display_stats())

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        for task in tasks:
            task.cancel()

        stats_task.cancel()
        await asyncio.sleep(1)

# Set up signal handling
signal.signal(signal.SIGINT, signal_handler)

# Command-line argument parsing
parser = argparse.ArgumentParser(description='WebSocket Stress Tester')
parser.add_argument('url', type=str, help='URL for the WebSocket server')
parser.add_argument('-c', '--connections', type=int, default=1, help='Number of connections to open simultaneously (default: 1)')
parser.add_argument('-m', '--messages', type=int, default=1, help='Number of messages to send per second (default: 1)')
parser.add_argument('-ch', '--characters', type=int, default=10, help='Number of characters per message (default: 10)')
args = parser.parse_args()

# Run the main function
try:
    asyncio.run(main(args.url, args.connections, args.messages, args.characters))
except websockets.exceptions.ConnectionClosedOK:
    print("\nConnection closed by the server")
except websockets.exceptions.InvalidURI:
    print("\nInvalid WebSocket server URL")
except ValueError:
    print("\nInvalid input provided")
