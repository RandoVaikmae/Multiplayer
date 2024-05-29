import socket
import pygame

client_pos = [400, 400]

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('172.20.10.3', 12345))
    
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: client_pos[0] -= 5
        if keys[pygame.K_RIGHT]: client_pos[0] += 5
        if keys[pygame.K_UP]: client_pos[1] -= 5
        if keys[pygame.K_DOWN]: client_pos[1] += 5
        
        client.send(f"{client_pos[0]},{client_pos[1]}".encode('utf-8'))
        server_pos = list(map(int, client.recv(1024).decode('utf-8').split(',')))

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (*client_pos, 50, 50))
        pygame.draw.rect(screen, (255, 0, 0), (*server_pos, 50, 50))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    client.close()

if __name__ == "__main__":
    start_client()
