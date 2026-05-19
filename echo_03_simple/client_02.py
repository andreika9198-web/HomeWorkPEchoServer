import socket

HOST = "127.0.0.1"
PORT = 50400

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        try:
            data_to_send = input('Ваше сообщение: ')
            if not  data_to_send.strip():
                continue
            message = data_to_send.upper()
            if  message == 'EXIT' or message == 'ВЫЙТИ':
                sock.sendall(data_to_send.encode())
                response = sock.recv(1024)
                print(f'Сервер: {response.decode()}')
                break
            data_bytes_to_send = data_to_send.encode()
            sock.sendall(data_bytes_to_send)
            data_bytes_received = sock.recv(1024)
            data_received = data_bytes_received.decode()
            print(f'Получено:', data_received)
        except  KeyboardInterrupt:
            print("Пользователь вышел из чата")
            data_to_send = 'EXIT'
            sock.sendall(data_to_send.encode())
            response = sock.recv(1024)
            print(f'Сервер: {response.decode()}')
            break
        except ConnectionAbortedError:
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break
        except ConnectionResetError:
            print('Сервер, в данный момент отключен пользователем')
            break