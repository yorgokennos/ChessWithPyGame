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


#load in each image
pieces = {
    'pawn_b': pygame.image.load("Pieces Images/pawn-b.svg"),
    'pawn_w': pygame.image.load("Pieces Images/pawn-w.svg"),
    'knight_b': pygame.image.load("Pieces Images/knight-b.svg"),
    'knight_w': pygame.image.load("Pieces Images/knight-w.svg"),
    'bishop_b': pygame.image.load("Pieces Images/bishop-b.svg"),
    'bishop_w': pygame.image.load("Pieces Images/bishop-w.svg"),
    'rook_b': pygame.image.load("Pieces Images/rook-b.svg"),
    'rook_w': pygame.image.load("Pieces Images/rook-w.svg"),
    'queen_b': pygame.image.load("Pieces Images/queen-b.svg"),
    'queen_w': pygame.image.load("Pieces Images/queen-w.svg"),
    'king_b': pygame.image.load("Pieces Images/king-b.svg"),
    'king_w': pygame.image.load("Pieces Images/king-w.svg")
}



#re-scale all the pieces
piece_size = 85

for key in pieces:
    pieces[key] = pygame.transform.scale(pieces[key], (piece_size,piece_size))


#offset based on square size and piece size
offset = (square_size - piece_size) // 2

#draw each black pawn
for i in range(8):
    surface.blit(pieces['pawn_b'], (i * square_size + offset, 1 * square_size + offset))

#draw each white pawn
for i in range(8):
    surface.blit(pieces['pawn_w'], (i * square_size + offset, 6 * square_size + offset))

#draw each rook
surface.blit(pieces['rook_b'], (0 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['rook_b'], (7 * square_size + offset, 0 + offset))
surface.blit(pieces['rook_w'], (0 * square_size + offset,7 * square_size + offset))
surface.blit(pieces['rook_w'], (7 * square_size + offset, 7 * square_size + offset ))

#draw each knight
surface.blit(pieces['knight_b'], (1 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['knight_b'], (6 * square_size + offset, 0 + offset))
surface.blit(pieces['knight_w'], (1 * square_size + offset, 7 * square_size + offset))
surface.blit(pieces['knight_w'], (6 * square_size + offset, 7 * square_size + offset ))

#draw each bishop
surface.blit(pieces['bishop_b'], (2 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['bishop_b'], (5 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['bishop_w'], (2 * square_size + offset, 7 * square_size + offset))
surface.blit(pieces['bishop_w'], (5 * square_size + offset, 7 * square_size + offset))

#draw both queens
surface.blit(pieces['queen_b'], (4 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['queen_w'], (4 * square_size + offset, 7 * square_size + offset))


#draw both kings
surface.blit(pieces['king_b'], (3 * square_size + offset, 0 * square_size + offset))
surface.blit(pieces['king_w'], (3 * square_size + offset, 7 * square_size + offset))


#"Render" drawings?????? CHECK THIS VERBAGE
pygame.display.flip()










while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    clock.tick(60)  # limits FPS to 60

pygame.quit()