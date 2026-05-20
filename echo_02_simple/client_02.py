import socket

HOST = "127.0.0.1"
PORT = 50432
##С помощью socket.socket() создаём объект сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Привязывает сокет к адресу и порту
    sock.connect((HOST, PORT))
    print('=' * 50)
    print('Информационная сноска')
    print("Для выхода из чата введите 'EXIT' или 'ВЫЙТИ'")
    print("Для остановки сервера введите 'STOP' или 'СТОП'")
    print('=' * 50)
    while True:
        try:
            #Пользователь вводит сообщение
            data_to_send = input('Ваше сообщение: ')
            #Проверка на пустое сообщение или сообщение с одними пробелами, и
            #заставляем пользователя повторно вводить сообщения
            if not  data_to_send.strip():
                continue
            #Полученные данные сохраняем верхнем регистре
            message = data_to_send.upper()
            #Проверка на выход
            if  message == 'EXIT' or message == 'ВЫЙТИ':
                #Отправляем сообщение на сервер
                sock.sendall(data_to_send.encode())
                #Получаем сообщение от сервера
                response = sock.recv(1024)
                print(f'Сервер: {response.decode()}')
                break
            #Преобразуем сообщения пользователя в байт
            data_bytes_to_send = data_to_send.encode()
            # Отправляем сообщение на сервер
            sock.sendall(data_bytes_to_send)
            #Сохраняем сообщение от сервера в переменную
            data_bytes_received = sock.recv(1024)
            #Преобразуем сообщение из байтов в строку и сохраняем в переменную
            data_received = data_bytes_received.decode()
            print(f'Получено:', data_received)
        except  KeyboardInterrupt:
            print("\nПользователь вышел из чата")
            #Ловим ошибку, и отправляем на сервер сообщение о выходе пользователя
            data_to_send = 'EXIT'
            #Отправляем сообщение на сервер
            sock.sendall(data_to_send.encode())
            #Получаем сообщение из сервера
            response = sock.recv(1024)
            print(f'Сервер: {response.decode()}')
            break
        except ConnectionAbortedError:
            # """
            #  Соглаcно условие дз:
            #  дать возможность по команде клиента выключить
            #  сервер, при этом клиент продолжает работу. Далее
            #  клиент отправляет отключенному серверу какое-нибудь сообщение,
            #  клиент не выпадает с ошибкой, а
            #  выдает сообщение о разрыве подключение и
            #  завершает работу с сообщением: “Process finished
            #  with exit code 0”
            #  """
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break
        except ConnectionResetError:
            print('Сервер, в данный момент отключен пользователем')
            break