import socket
import threading

HOST = "127.0.0.1"
PORT = 50400
stop_server = False

def handle_connection(sock, addr):
    """
    Функция для обработки подключения клиента в отдельном потоке.

    Аргументы:
        sock: сокет для общения с клиентом
        addr: адрес клиента (IP, порт)
    """
    #Используем глобальную переменную, для остановки сервера
    global stop_server
    #Автоматически закрывает сокет в конце блока
    with sock:
        print('Подключение по адресу:', addr)

        while True:
            # Receive
            try:
                #Получаем данные из сокета, и сохраняем в переменную
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
                # Декодируем байты в строку и убираем лишние пробелы
                message = data.decode().strip().upper()
                print(f'проверка {message}')

                # Отключаем пользователя от сервера, но сервер работает
                if message == 'EXIT' or message == 'ВЫЙТИ':
                    # Отправляем данные пользователю
                    sock.sendall("Вы отключены от сервера. До свидания!".encode())
                    print(f'Клиент {addr} отключился по команде {message}')
                    return False
                    # Отключаем пользователя от сервера, но сервер работает
                elif message == 'STOP' or message == 'СТОП':
                    # Отправляем данные пользователю
                    sock.sendall("Вы отключили  сервер. До свидания, сервер!".encode())
                    print(f'Клиент {addr} отключил по команде {message}')
                    # Флаг, указывает что сервер не нужно остановить
                    stop_server = True
                    return False
            print(f'Получено: {data}, от {addr}')
            # Полученные данные сохраняем верхнем регистре
            data = data.upper()
            print(f'Отправлено: {data}, по адресу: {addr}')

            try:
                # Отправляем данные пользователю
                sock.sendall(data)
            except ConnectionError:
                print(f'Клиент внезапно отключился не могу отправить данные')


if __name__ == '__main__':
    # С помощью socket.socket() создаём объект сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        # Привязывает сокет к адресу и порту
        serv_socket.bind((HOST, PORT))
        # Переводим сокет в режим ожидания подключений (серверный режим)
        serv_socket.listen()
        # Устанавливаем таймаут (время ожидания) для операций с сокетом
        serv_socket.settimeout(1.0)
        # Список для хранения потоков
        threads = []
        print('Ожидаю соединения...')
        try:
            while not stop_server:
                try:
                    #Принимает входящее подключение (блокирующий вызов)
                    sock_, addr_ = serv_socket.accept()
                    #Создаем поток
                    thread = threading.Thread(target=handle_connection,args=(sock_, addr_))
                    #Делаем поток фоновым
                    thread.daemon = True
                    #Запускаем потоки
                    thread.start()
                    # Добавляем поток в список
                    threads.append(thread)
                    # Выходим из цикла
                    if stop_server:
                        break
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nПолучен сигнал остановки сервера")
            stop_server = True

        # ожидаем завершения потока t не более 1 секунды.
        for t in threads:
            t.join(timeout=1)
        print("Сервер полностью остановлен")