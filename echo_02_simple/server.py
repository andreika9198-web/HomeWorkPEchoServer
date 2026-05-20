import socket

HOST = "127.0.0.1"
PORT = 50432

if __name__ == '__main__':
    #С помощью socket.socket() создаём объект сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        #Привязывает сокет к адресу и порту
        serv_socket.bind((HOST, PORT))
        #Переводит сокет в режим ожидания подключений (серверный режим)
        serv_socket.listen()
        #Флаг, указывает что сервер находиться в работе
        my_server = True
        while my_server:
            print('Ожидаю соединения...')
            #Принимает входящее подключение (блокирующий вызов)
            sock, addr = serv_socket.accept()
            #Автоматически закрывает сокет в конце блока
            with sock:
                print('Подключение по адресу:', addr)
                while True:
                    # Receive
                    try:
                        #Получаем данные из сокета, 1024 — это размер буфера в байтах
                        data = sock.recv(1024)
                        if not data:
                            print(f'Клиент {addr} отключился')
                            break
                        #Получаем сообщение от пользователя в байтах и преобразуем в строку
                        message = data.decode().strip().upper()
                        print(f'проверка {message}')
                        #Отключаем пользователя от сервера, но сервер работает
                        if message  == 'EXIT' or message == 'ВЫЙТИ':
                            #Отправляем данные на сервер
                            sock.sendall("Вы отключены от сервера. До свидания!".encode())
                            print(f'Клиент {addr} отключился по команде {message}')
                            break
                        # Отключаем пользователя от сервера, но сервер работает
                        elif  message  == 'STOP' or message == 'СТОП':
                            # Отправляем данные на сервер
                            sock.sendall("Вы отключили  сервер. До свидания, сервер!".encode())
                            print(f'Клиент {addr} отключил по команде {message}')
                            #Флаг, указывает что сервер не нужно остановить
                            my_server = False
                            break


                    except ConnectionError:
                        print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
                        break
                    except KeyboardInterrupt:
                        print("\nСервер остановлен пользователем")
                        break

                    print(f'Получено: {data}, от {addr}')
                    #Полученные данные сохраняем верхнем регистре
                    data = data.upper()
                    print(f'Отправлено: {data}, по адресу: {addr}')

                    try:
                        #Отправляем данные на сервер
                        sock.sendall(data)
                    except ConnectionError:
                        print(f'Клиент внезапно отключился не могу отправить данные')
        print("Отключение по")

