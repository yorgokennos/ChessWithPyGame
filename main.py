# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
pygame.display.set_caption("Chess by Yorgo")
surface = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True


#colors of the board
color_dark_green = (118, 150, 86)
color_light_green = (238, 238, 210)


#size of each square
square_size = 90


#draw the board
#   doing this outside of the running loop since board will be the same every game
for x in range(8):
    for y in range(8):
        if (x+ y) % 2 == 0:
            pygame.draw.rect(surface, color_dark_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
        else:
            pygame.draw.rect(surface, color_light_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))


#update surface to the screen
pygame.display.flip()


#changing pieces changing it to be a dictionary, of  dictionaries
#   this way I have each piece, and it's location which I can update and keep track of
pieces = {
    'pawn_b1': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (0, 1)},
    'pawn_b2': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (1, 1)},
    'pawn_b3': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (2, 1)},
    'pawn_b4': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (3, 1)},
    'pawn_b5': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (4, 1)},
    'pawn_b6': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (5, 1)},
    'pawn_b7': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (6, 1)},
    'pawn_b8': {'image': pygame.image.load("Pieces Images/pawn-b.svg"), 'position': (7, 1)},

    'pawn_w1': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (0, 6)},
    'pawn_w2': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (1, 6)},
    'pawn_w3': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (2, 6)},
    'pawn_w4': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (3, 6)},
    'pawn_w5': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (4, 6)},
    'pawn_w6': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (5, 6)},
    'pawn_w7': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (6, 6)},
    'pawn_w8': {'image': pygame.image.load("Pieces Images/pawn-w.svg"), 'position': (7, 6)},

    'knight_b1': {'image': pygame.image.load("Pieces Images/knight-b.svg"), 'position': (1, 0)},
    'knight_b2': {'image': pygame.image.load("Pieces Images/knight-b.svg"), 'position': (6, 0)},

    'knight_w1': {'image': pygame.image.load("Pieces Images/knight-w.svg"), 'position': (1, 7)},
    'knight_w2': {'image': pygame.image.load("Pieces Images/knight-w.svg"), 'position': (6, 7)},

    'bishop_b1': {'image': pygame.image.load("Pieces Images/bishop-b.svg"), 'position': (2, 0)},
    'bishop_b2': {'image': pygame.image.load("Pieces Images/bishop-b.svg"), 'position': (5, 0)},
    
    'bishop_w1': {'image': pygame.image.load("Pieces Images/bishop-w.svg"), 'position': (2, 7)},
    'bishop_w2': {'image': pygame.image.load("Pieces Images/bishop-w.svg"), 'position': (5, 7)},

    'rook_b1': {'image': pygame.image.load("Pieces Images/rook-b.svg"), 'position': (0, 0)},
    'rook_b2': {'image': pygame.image.load("Pieces Images/rook-b.svg"), 'position': (7, 0)},
    
    'rook_w1': {'image': pygame.image.load("Pieces Images/rook-w.svg"), 'position': (0, 7)},
    'rook_w2': {'image': pygame.image.load("Pieces Images/rook-w.svg"), 'position': (7, 7)},

    'queen_b': {'image': pygame.image.load("Pieces Images/queen-b.svg"), 'position': (3, 0)},
    'queen_w': {'image': pygame.image.load("Pieces Images/queen-w.svg"), 'position': (3, 7)},

    'king_b': {'image': pygame.image.load("Pieces Images/king-b.svg"), 'position': (4, 0)},
    'king_w': {'image': pygame.image.load("Pieces Images/king-w.svg"), 'position': (4, 7)}
}



#scale for pieces size
piece_size = 85

#offset based on square size and piece size
offset = (square_size - piece_size) // 2


#resize each image via for loop
for key in pieces:
    pieces[key]['image'] = pygame.transform.scale(pieces[key]['image'], (piece_size, piece_size))



# draw the pieces
for piece_key, piece in pieces.items():
    surface.blit(piece['image'], (piece['position'][0] * square_size + offset, piece['position'][1] * square_size + offset))


#"Render" drawings?????? CHECK THIS VERBAGE
pygame.display.flip()



#print the position (x, y) of each piece
print( square_size * pieces['pawn_b1']['position'][0] + offset)
print( square_size * pieces['pawn_b1']['position'][1] + offset)


# rectangular "view" of piece
pawn_b1_rect = pieces['pawn_b1']['image'].get_rect()
pawn_b1_rect.topleft = (pieces['pawn_b1']['position'][0] * square_size + offset, pieces['pawn_b1']['position'][1] * square_size + offset)

print(pawn_b1_rect.topleft)
print(pawn_b1_rect.topright)
print(pawn_b1_rect.bottomleft)
print(pawn_b1_rect.bottomright)


while running:

    #setting cursor for fun
    pygame.mouse.set_cursor(*pygame.cursors.diamond)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #detecting left mouse press down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #1 = left_mouse   2 = scroll  3 = right_mouse
                print("left mouse button pressed")
                mx, my = pygame.mouse.get_pos()
                print( pygame.mouse.get_pos())

                #check if mouse press is on a piece
                if pawn_b1_rect.collidepoint(mx, my):
                    #change color of "piece" clicked
                    pygame.draw.rect(surface, (255, 0, 0), pawn_b1_rect)  # Draw red rectangle over the piece_rect area
                    pygame.display.flip()
        
        #detecting left mouse depress
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                print("left mouse has been de-pressed")
                print( pygame.mouse.get_pos())



    #[left_button, #scroll_button, #right_button]
    #[bool, bool, bool]
    #print(pygame.mouse.get_pressed())

    clock.tick(60)  # limits FPS to 60

pygame.quit()
