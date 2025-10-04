import pygame as py
import os

py.init() #lance pygame

window = py.display.set_mode((820, 680)) #cree une fenetre
py.display.set_caption("chess") #titre de la fenêtre
clock = py.time.Clock() #gere les FPS

#definit les couleurs (RGB)
WHITE = (255, 255, 255)
BLACK = (101, 63, 33)
GREY = (150, 150, 150)

#jeu
game = False

#timers
time_j1, time_j2 = 600, 600 #10 minutes
timer_j1, timer_j2 = True, False
text = py.font.Font(None, 60) #police d'ecriture

class Piece(py.sprite.Sprite):
    def __init__(self, image_path, position, case_size, color):
        super().__init__()
        try:
            image = py.image.load(image_path).convert_alpha()

            #redimensionne l'image pour tenir dans une case
            self.image = py.transform.smoothscale(image, (case_size, case_size))
            self.rect = self.image.get_rect(topleft=position)
            self.color = color #"blanc" ou "noir"
        except:
            #si l'image ne charge pas, cree une surface rouge transparente
            self.image = py.Surface((case_size, case_size), py.SRCALPHA)
            self.image.fill((255, 0, 0, 128))
            self.rect = self.image.get_rect(topleft=position)
            self.color = color

img_dir = r"c:\\Users\\amaca\\Documents\\pychess"

#place toutes les pieces à leur emplacement original
pieces_positions = [
    [["tour_noir.png", "noir"], ["cavalier_noir.png", "noir"], ["fou_noir.png", "noir"], ["reine_noir.png", "noir"],
     ["roi_noir.png", "noir"], ["fou_noir.png", "noir"], ["cavalier_noir.png", "noir"], ["tour_noir.png", "noir"]],
    [["pion_noir.png", "noir"]] * 8,
    [[None, None]] * 8,
    [[None, None]] * 8,
    [[None, None]] * 8,
    [[None, None]] * 8,
    [["pion_blanc.png", "blanc"]] * 8,
    [["tour_blanc.png", "blanc"], ["cavalier_blanc.png", "blanc"], ["fou_blanc.png", "blanc"],
     ["reine_blanc.png", "blanc"], ["roi_blanc.png", "blanc"], ["fou_blanc.png", "blanc"],
     ["cavalier_blanc.png", "blanc"], ["tour_blanc.png", "blanc"]],
]

#affiche les pieces
pieces_group = py.sprite.Group()
case_x = window.get_width() // 8 - 20
case_y = window.get_height() // 8
case_size = min(case_x, case_y)
for row in range(8):
    for col in range(8):
        piece_info = pieces_positions[row][col]
        if piece_info[0]:
            img_path = os.path.join(img_dir, piece_info[0])
            pos = (col * case_x, row * case_y)
            piece = Piece(img_path, pos, case_size, piece_info[1])
            pieces_group.add(piece)

selected_piece = None
offset_x, offset_y = 0, 0

#le jeu
while True:
    for event in py.event.get(): #recupere les events
        if event.type == py.QUIT: #si on clique sur la croix
            py.quit()
            exit()
        elif event.type == py.KEYDOWN and event.key == py.K_SPACE and not game:
            game = True
        elif event.type == py.KEYDOWN and event.key == py.K_SPACE and game:
            timer_j1 = not timer_j1
            timer_j2 = not timer_j2
        elif event.type == py.MOUSEBUTTONDOWN and game:
            if event.button == 1:
                for piece in pieces_group:
                    if piece.rect.collidepoint(event.pos):
                        selected_piece = piece
                        offset_x = piece.rect.x - event.pos[0]
                        offset_y = piece.rect.y - event.pos[1]
                        break
        elif event.type == py.MOUSEBUTTONUP and game:
            if event.button == 1 and selected_piece:

                #trouver la case
                col = selected_piece.rect.centerx // case_x
                row = selected_piece.rect.centery // case_y

                #coin superieur gauche de cette case
                new_x = col * case_x
                new_y = row * case_y

                #verifie si une piece est deja sur cette case
                for piece in pieces_group:
                    if piece != selected_piece and piece.rect.collidepoint(new_x, new_y):

                        #supprime la pièce mangée si elle est de couleur opposée
                        if piece.color != selected_piece.color:
                            pieces_group.remove(piece)
                        break

                #recentre la piece dans la case
                selected_piece.rect.topleft = (new_x, new_y)
                selected_piece = None
        elif event.type == py.MOUSEMOTION:
            if selected_piece:
                selected_piece.rect.x = event.pos[0] + offset_x
                selected_piece.rect.y = event.pos[1] + offset_y

    #le menu
    if not game:
        window.fill(GREY)
        intro_text = text.render("press 'space' to start", True, BLACK)
        window.blit(intro_text, (50, window.get_height() // 2 - 30))
        py.display.flip()
        keys = py.key.get_pressed()
        if keys[py.K_SPACE]:
            game = True
    
    #l'echiquier
    elif game:
        if timer_j1:
            time_j1 -= 1/60 #pour les 60 FPS
        elif timer_j2:
            time_j2 -= 1/60
        window.fill(GREY) #remplit la fenetre avec la couleur grise
        #dessiner la grille 8x8
        taille_case_x = window.get_width() // 8 - 20
        taille_case_y = window.get_height() // 8
        
        #dessine les cases
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = (col * taille_case_x, row * taille_case_y, taille_case_x, taille_case_y)
                py.draw.rect(window, color, rect)

        #affiche les timers
        py.draw.rect(window, GREY, (805, 10, 10, 20))
        timer_text = text.render(f"{int(time_j1)}", True, BLACK)
        window.blit(timer_text, (720, 10))
        py.draw.rect(window, GREY, (805, 50, 10, 20))
        timer_text2 = text.render(f"{int(time_j2)}", True, BLACK)
        window.blit(timer_text2, (720, 630))

        pieces_group.draw(window) #dessine toutes les pieces
        py.display.flip() #met à jour l'affichage
    clock.tick(60) #FPS

#magnus carlsen 2024-06
#version 0.8