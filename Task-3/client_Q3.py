import socket
import time
import argparse

def send_data_at_rate(server_ip='10.0.211.79', port=8080,
                      disable_nagle=False, disable_delayed_ack=False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Disable Nagle's algorithm if requested
    if disable_nagle:
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print("Nagle's algorithm has been disabled (TCP_NODELAY set).")

    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")

        # Disable delayed ACK if requested and supported    
        if disable_delayed_ack:
            if hasattr(socket, 'TCP_QUICKACK'):
                try:
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                    print("Delayed ACK has been disabled (TCP_QUICKACK set).")
                except Exception as e:
                    print("Could not disable delayed ACK:", e)
            else:
                print("Disabling delayed ACK is not supported on this system.")

        data = 'A' * 4096  # Prepare 4KB of data
        bytes_sent = 0

        # Send data in chunks to match the specified rate
        chunk_size = 40  # number of bytes per interval
        interval = 0.001  # seconds between chunks

        while bytes_sent < 4096:
            # Calculate how many bytes to send in this round
            current_chunk_size = chunk_size
            if bytes_sent + current_chunk_size > 4096:
                current_chunk_size = 4096 - bytes_sent  # send the remaining bytes

            chunk = data[bytes_sent:bytes_sent + current_chunk_size]
            client_socket.sendall(chunk.encode('utf-8'))
            bytes_sent += len(chunk)

            print(f"Sent {len(chunk)} bytes, Total sent: {bytes_sent}/{4096} bytes")
            time.sleep(interval)

        print("Finished sending all data.")

        # Optionally, receive server response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Send data at a specified rate with options to disable Nagle's algorithm and delayed ACK."
    )
    parser.add_argument("--server-ip", type=str, default='10.0.211.79', help="Server IP address")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--disable-nagle", action="store_true", help="Disable Nagle's algorithm (TCP_NODELAY)")
    parser.add_argument("--disable-delayed-ack", action="store_true", help="Disable delayed ACK (if supported)")

    args = parser.parse_args()

    send_data_at_rate(
        server_ip=args.server_ip,
        port=args.port,
        disable_nagle=args.disable_nagle,
        disable_delayed_ack=args.disable_delayed_ack
    )
