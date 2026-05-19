import socket
import threading

HOST = "127.0.0.1"
PORT = 50400
stop_server = False

def handle_connection(sock, addr):
    global stop_server
    with sock:
        print('Подключение по адресу:', addr)

        while True:
            # Receive
            try:
                data = sock.recv(1024)

            except ConnectionError:
                print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
                return False
            except KeyboardInterrupt:
                print("\nСервер остановлен пользователем")
                return False
            else:
                if not data:
                    print(f'Клиент {addr} отключился')
                    return False
                message = data.decode().strip().upper()
                print(f'проверка {message}')

                if message == 'EXIT' or message == 'ВЫЙТИ':
                    sock.sendall("Вы отключены от сервера. До свидания!".encode())
                    print(f'Клиент {addr} отключился по команде {message}')

                elif message == 'STOP' or message == 'СТОП':
                    sock.sendall("Вы отключили  сервер. До свидания, сервер!".encode())
                    print(f'Клиент {addr} отключил по команде {message}')
                    stop_server = True
                    return False
            print(f'Получено: {data}, от {addr}')
            data = data.upper()
            print(f'Отправлено: {data}, по адресу: {addr}')

            try:
                sock.sendall(data)
            except ConnectionError:
                print(f'Клиент внезапно отключился не могу отправить данные')


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        serv_socket.bind((HOST, PORT))
        serv_socket.listen()
        serv_socket.settimeout(1.0)
        threads = []
        print('Ожидаю соединения...')
        while not stop_server:
            try:
                sock_, addr_ = serv_socket.accept()
                thread = threading.Thread(target=handle_connection,args=(sock_, addr_))
                thread.daemon = True
                thread.start()
                threads.append(thread)
                if stop_server:
                    break
            except socket.timeout:
                continue
        for t in threads:
            t.join(timeout=1)  # Ждём максимум 1 секунду