import pygame

#pygame initialization
pygame.init()
pygame.display.set_caption("Chess by Yorgo")
surface = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

#cboard setup
color_dark_green = (118, 150, 86)
color_light_green = (238, 238, 210)
square_size = 90
offset = (square_size - 85) // 2 #assuming piece size is 85


###PIECE CLASS ####
class Piece:
    def __init__(self, image_path, position, square_size, offset):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (square_size - offset * 2, square_size - offset * 2)) 
        self.position = position
        self.square_size = square_size
        self.offset = offset
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0] * square_size + offset, position[1] * square_size + offset) 

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def move(self, new_position):
        self.position = new_position
        self.rect.topleft = (new_position[0] * self.square_size + self.offset, new_position[1] * self.square_size + self.offset)


#funciton to draw the board
def draw_board():
    for x in range(8):
        for y in range(8):
            if (x+ y) % 2 == 0:
                pygame.draw.rect(surface, color_dark_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            else:
                pygame.draw.rect(surface, color_light_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))



#dictionary with Piece class
pieces = {
    'pawn_b1': Piece("Pieces Images/pawn-b.svg", (0, 1), square_size, offset),
    'pawn_b2': Piece("Pieces Images/pawn-b.svg", (1, 1), square_size, offset),
    'pawn_b3': Piece("Pieces Images/pawn-b.svg", (2, 1), square_size, offset),
    'pawn_b4': Piece("Pieces Images/pawn-b.svg", (3, 1), square_size, offset),
    'pawn_b5': Piece("Pieces Images/pawn-b.svg", (4, 1), square_size, offset),
    'pawn_b6': Piece("Pieces Images/pawn-b.svg", (5, 1), square_size, offset),
    'pawn_b7': Piece("Pieces Images/pawn-b.svg", (6, 1), square_size, offset),
    'pawn_b8': Piece("Pieces Images/pawn-b.svg", (7, 1), square_size, offset),

    'pawn_w1': Piece("Pieces Images/pawn-w.svg", (0, 6), square_size, offset),
    'pawn_w2': Piece("Pieces Images/pawn-w.svg", (1, 6), square_size, offset),
    'pawn_w3': Piece("Pieces Images/pawn-w.svg", (2, 6), square_size, offset),
    'pawn_w4': Piece("Pieces Images/pawn-w.svg", (3, 6), square_size, offset),
    'pawn_w5': Piece("Pieces Images/pawn-w.svg", (4, 6), square_size, offset),
    'pawn_w6': Piece("Pieces Images/pawn-w.svg", (5, 6), square_size, offset),
    'pawn_w7': Piece("Pieces Images/pawn-w.svg", (6, 6), square_size, offset),
    'pawn_w8': Piece("Pieces Images/pawn-w.svg", (7, 6), square_size, offset),

    'knight_b1': Piece("Pieces Images/knight-b.svg", (1, 0), square_size, offset),
    'knight_b2': Piece("Pieces Images/knight-b.svg", (6, 0), square_size, offset),

    'knight_w1': Piece("Pieces Images/knight-w.svg", (1, 7), square_size, offset),
    'knight_w2': Piece("Pieces Images/knight-w.svg", (6, 7), square_size, offset),

    'bishop_b1': Piece("Pieces Images/bishop-b.svg", (2, 0), square_size, offset),
    'bishop_b2': Piece("Pieces Images/bishop-b.svg", (5, 0), square_size, offset),
    
    'bishop_w1': Piece("Pieces Images/bishop-w.svg", (2, 7), square_size, offset),
    'bishop_w2': Piece("Pieces Images/bishop-w.svg", (5, 7), square_size, offset),

    'rook_b1': Piece("Pieces Images/rook-b.svg", (0, 0), square_size, offset),
    'rook_b2': Piece("Pieces Images/rook-b.svg", (7, 0), square_size, offset),
    
    'rook_w1': Piece("Pieces Images/rook-w.svg", (0, 7), square_size, offset),
    'rook_w2': Piece("Pieces Images/rook-w.svg", (7, 7), square_size, offset),

    'queen_b': Piece("Pieces Images/queen-b.svg", (3, 0), square_size, offset),
    'queen_w': Piece("Pieces Images/queen-w.svg", (3, 7), square_size, offset),

    'king_b': Piece("Pieces Images/king-b.svg", (4, 0), square_size, offset),
    'king_w': Piece("Pieces Images/king-w.svg", (4, 7), square_size, offset)
}


#draw pieces
for piece in pieces.values():
    piece.draw(surface)

pygame.display.flip()



#variables needed for click/dragging
dragging_piece = None
drag_offset_x = 0
drag_offset_y = 0

##main game loop
running = True
while running:

    #setting cursor for fun
    pygame.mouse.set_cursor(*pygame.cursors.diamond)

    # poll for events
    for event in pygame.event.get():

        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False


        #detecting left mouse press down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #1 = left_mouse   2 = scroll  3 = right_mouse
                print("left mouse button pressed")
                mx, my = pygame.mouse.get_pos()
                print( pygame.mouse.get_pos())
                for piece_key, piece in pieces.items():
                    if piece.rect.collidepoint(mx, my):
                        dragging_piece = piece
                        drag_offset_x = piece.rect.x - mx
                        drag_offset_y = piece.rect.y - my
                        break

        #detecting left mouse UP
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_piece is not None:
                mx, my = pygame.mouse.get_pos()
                new_position = (mx // square_size, my // square_size)
                dragging_piece.move(new_position)
                dragging_piece = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_piece is not None:
                mx, my = event.pos
                dragging_piece.rect.topleft = (mx + drag_offset_x, my + drag_offset_y)
                
    
    #re-draw board and pieces
    draw_board()

    for piece in pieces.values():
        piece.draw(surface)
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

