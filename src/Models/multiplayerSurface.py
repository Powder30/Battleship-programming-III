import pygame
from src.Link.connection import Conexion
import socket
import threading

class MultiplayerSurface:
    def __init__(self, title, width, height, colorT):
        
        pygame.font.init()
        self.title = title
        self.width = width
        self.height = height
        self.colorT=colorT
        self.surface = pygame.Surface((width, height))
        self.surface.fill((3, 37, 108))
        self.backSur= pygame.image.load("6292.jpg")
        self.backSur = pygame.transform.scale(self.backSur, (self.width, self.height))
        self.font_tittle= pygame.font.Font(None, 36)
        self.state = "host"
        self.conexion= None
        self.server_thread = None
        self.font = pygame.font.Font(None, 24)
        self.ip = Conexion.get_local_ip()  
        self.puerto = 5555  
        self.sock = None
        self.input_text = ""
        self.input_active = False
        self.input_rect = pygame.Rect(width//2 - 100, 200, 200, 32)
        self.font_input = pygame.font.Font(None, 32)
        

        
        
        
        
        
        
  
    def draw(self):
        self.surface.fill((3, 37, 108))
        self.surface.blit(self.backSur,(0,0))

        # dibujar el título
        title = self.font_tittle.render(self.title, True, self.colorT )
        title_rect = title.get_rect(center=(self.width // 2, 25))
        self.surface.blit(title, title_rect)

        
        if self.state == "host":
            self.draw_host()
        elif self.state == "hosting":
            self.draw_hosting()
        else: 
            self.state == "join"
            self.draw_join()
        

    def draw_host(self):
    # Fondo y título
     self.surface.blit(self.backSur, (0, 0))
     title = self.font_tittle.render("Multiplayer Menu", True, (255, 255, 255))
     self.surface.blit(title, (self.width // 2 - title.get_width() // 2, 50))

    # Botón "Hosting Game "
     self.btnHost = pygame.draw.rect(self.surface, (255, 0, 0), (self.width // 2 - 100, 200, 200, 50))
     host_text = self.font.render("Host", True, (255, 255, 255))
     self.surface.blit(host_text, (self.width // 2 - host_text.get_width() // 2, 215))
     #Boton "Join Game"
     self.buttonJoin = pygame.draw.rect(self.surface, (255, 0, 0), (self.width // 2 - 100, 300, 200, 50))
     join_text = self.font.render("Join", True, (255, 255, 255))
     self.surface.blit(join_text, (self.width // 2 - join_text.get_width() // 2, 315))

    # Información de conexión 
     info_text = self.font.render("Waiting for players...", True, (255, 255, 255))
     self.surface.blit(info_text, (self.width // 2 - info_text.get_width() // 2, 400))
     

    # Instrucciones
     instructions = [
        "Host controls:",
        "- Press 'host' to hosting a game",
        "- Press 'join' to join a game",
     ]
     for i, line in enumerate(instructions):
        text = self.font.render(line, True, (255, 255, 255))
        self.surface.blit(text, (50, 400 + i * 30))
    
    
        
    def draw_hosting(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.backSur, (0, 0))
        title = self.font_tittle.render("Hosting menu", True, (255, 255, 255))
        self.surface.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        hostData = Conexion.get_local_ip()
        hostText = self.font.render(f'User ip: {hostData}  puerto:5500', True, (255, 255, 255))
        self.surface.blit(hostText, (self.width // 2 - hostText.get_width() // 2, 100))
        conexion_Text = self.font.render("Waiting for players...", True, (255, 255, 255))
        self.surface.blit(conexion_Text, (self.width // 2 - conexion_Text.get_width() // 2, 400))
    def draw_join(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.backSur, (0, 0))
        title = self.font_tittle.render("Unirse a Partida", True, (255, 255, 255))
        self.surface.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        # Dibuja la caja de texto
        color = pygame.Color('dodgerblue2') if self.input_active else pygame.Color('lightskyblue3')
        pygame.draw.rect(self.surface, color, self.input_rect, 2)
        
        # Dibuja el texto ingresado
        text_surface = self.font_input.render(self.input_text, True, (255, 255, 255))
        self.surface.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        
        instr = self.font.render("Ingresa IP del servidor y presiona Enter", True, (255, 255, 255))
        self.surface.blit(instr, (self.width//2 - instr.get_width()//2, 150))

            
    def handle_events(self, events):
        for event in events:
            if self.state == "join":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activar/desactivar la caja de texto
                    self.input_active = self.input_rect.collidepoint(event.pos)
                
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        print(f"IP ingresada: {self.input_text}")
                        try:
                             self.conexion = Conexion(
                            modo_servidor=False,
                            ip=self.input_text,
                            puerto=5555 )
                             print("¡Conectado al servidor!")
                        except Exception as e:
                              print(f"Error de conexión: {e}")
                
                       
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 15:  
                            self.input_text += event.unicode
                            
        
        
                                
    def handle_click(self, mouse_pos):
        if self.state == "host":
            if hasattr(self, 'btnHost') and self.btnHost.collidepoint(mouse_pos):
                self.state = "hosting"
                self.draw_hosting()
                # Crea y configura la conexión como servidor
                try:
                    self.conexion = Conexion(modo_servidor=True, ip=self.ip, puerto=self.puerto)
                
                # Inicia el servidor en un hilo separado para no bloquear la UI
                    self.server_thread = threading.Thread(
                    target=self.conexion._iniciar_como_servidor,
                    daemon=True
                   )
                    self.server_thread.start()
                
                    return "hosting"
                except Exception as e:
                   print(f"Error al iniciar servidor: {e}")
                   self.state = "host"  # Vuelve al estado anterior
                   return None
        
           
    
            elif hasattr(self, 'buttonJoin') and self.buttonJoin.collidepoint(mouse_pos):
                 self.state = "join"
                 self.state = "join"
                 self.input_text = ""  
                 self.input_active = True  
                 self.draw_join()
                 return "join"
             
          
            
        return None
     