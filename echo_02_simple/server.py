import socket

HOST = "127.0.0.1"
PORT = 50432

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        serv_socket.bind((HOST, PORT))
        serv_socket.listen()
        my_server = True
        while my_server:
            print('Ожидаю соединения...')
            sock, addr = serv_socket.accept()
            with sock:
                print('Подключение по адресу:', addr)
                while True:
                    # Receive
                    try:
                        data = sock.recv(1024)
                        if not data:
                            print(f'Клиент {addr} отключился')
                            break
                        message = data.decode().strip().upper()
                        print(f'проверка {message}')

                        if message  == 'EXIT' or message == 'ВЫЙТИ':
                            sock.sendall("Вы отключены от сервера. До свидания!".encode())
                            print(f'Клиент {addr} отключился по команде {message}')
                            break
                        elif  message  == 'STOP' or message == 'СТОП':
                            sock.sendall("Вы отключили  сервер. До свидания, сервер!".encode())
                            print(f'Клиент {addr} отключил по команде {message}')
                            my_server = False
                            break


                    except ConnectionError:
                        print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
                        break
                    except KeyboardInterrupt:
                        print("\nСервер остановлен пользователем")
                        break

                    print(f'Получено: {data}, от {addr}')
                    data = data.upper()
                    print(f'Отправлено: {data}, по адресу: {addr}')

                    try:
                        sock.sendall(data)
                    except ConnectionError:
                        print(f'Клиент внезапно отключился не могу отправить данные')
        print("Отключение по")

