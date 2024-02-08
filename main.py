import socket

host = "0.0.0.0"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(1)

client_socket, client_address = server_socket.accept()

def response(status_code: int, status_text: str, headers: dict, body: str) -> str:
    response = f"HTTP/1.1 {status_code} {status_text}\r\n"
    headers["Content-Length"] = str(len(body))
    for key, value in headers.items():
        response += f"{key}: {value}\r\n"
    response += "\r\n"
    response += body
    return response

def handle(mathod: str, path: str, headers: dict) -> str:
    try:
        f = open(path.removeprefix("/"), 'r')
        return response(
            200,
            "OK",
            {
                "Content-Type": "text/html",
            },
            f.read().replace("{hello world}", "hello from server")
        )
    except:
        return response(404, "Not Found", {}, "")

def request(data: str) -> str:
    lines = data.splitlines()
    first_line = lines[0]
    method, path, _ = first_line.split()
    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(': ')
        headers[key] = value
    
    return handle(method, path, headers)

while True:
    data = client_socket.recv(2048)
    if not data:
        break
    response_to_client = request(str(data.decode('utf-8')))
    client_socket.send(response_to_client.encode())

client_socket.close()
server_socket.close()