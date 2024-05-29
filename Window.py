import pygame
import threading
import socket

positions = {'server': [100, 100], 'client': [400, 400]}

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                positions['client'] = list(map(int, data.split(',')))
                client_socket.send(f"{positions['server'][0]},{positions['server'][1]}".encode('utf-8'))
            else:
                break
        except:
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('172.20.10.3', 12345))
    server.listen(5)
    print("Server started, waiting for connections...")
    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    threading.Thread(target=start_server, daemon=True).start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: positions['server'][0] -= 5
        if keys[pygame.K_d]: positions['server'][0] += 5
        if keys[pygame.K_w]: positions['server'][1] -= 5
        if keys[pygame.K_s]: positions['server'][1] += 5

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (*positions['server'], 50, 50))
        pygame.draw.rect(screen, (0, 255, 0), (*positions['client'], 50, 50))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
