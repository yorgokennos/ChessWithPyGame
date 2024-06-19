import pygame

#pygame initialization
pygame.init()
pygame.display.set_caption("Chess by Yorgo")
surface = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

#board setup
color_dark_green = (118, 150, 86)
color_light_green = (238, 238, 210)
square_size = 90
offset = (square_size - 85) // 2 #assuming piece size is 85

###PIECE CLASS ####
class Piece:
    def __init__(self, image_path, position, square_size, offset, piece_type, color):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (square_size - offset * 2, square_size - offset * 2)) 
        self.position = position
        self.square_size = square_size
        self.offset = offset
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0] * square_size + offset, position[1] * square_size + offset)
        self.piece_type = piece_type
        self.color = color

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def move(self, new_position):
        self.position = new_position
        self.rect.topleft = (new_position[0] * self.square_size + self.offset, new_position[1] * self.square_size + self.offset)

def is_valid_pawn_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    #consider if the piece is black or white
    direction = -1 if piece.color == 'w' else 1
    start_row = 6 if piece.color == 'w' else 1

    # Check if move is forward
    if start_x == end_x:
        # Move forward one square
        if end_y - start_y == direction and (end_x, end_y) not in pieces:
            return True
        # Move forward two squares from starting position
        if start_y == start_row and end_y - start_y == 2 * direction and (end_x, end_y) not in pieces and (end_x, start_y + direction) not in pieces:
            return True
    # Check if move is diagonal capture
    elif abs(start_x - end_x) == 1 and end_y - start_y == direction and (end_x, end_y) in pieces and pieces[(end_x, end_y)].color != piece.color:
        return True

    return False

def is_valid_knight_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    #check if move forms L shape
    if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
        #destination square is empty or contains opponent's piece
        if(end_x, end_y) not in pieces or pieces[(end_x - end_y)].color != piece.color:
            return True
    
    return False

def is_valid_bishop_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    #check if movement is diagonal
    if(dx == dy):

        #direction of movement
        step_x = 1 if end_x > start_x else -1
        step_y = 1 if end_y > start_y else -1

        #check if path is clear
        x, y = start_x + step_x, start_y + step_y
        while x != end_x and y != end_y:
            if (x, y) in pieces:
                return False
            x += step_x
            y += step_y


        #check if empty or has opponent's piece
        if(end_x, end_y) not in pieces or pieces[(end_x - end_y)].color != piece.color:
            return True
        
    return False

def is_valid_rook_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    #check if movement is vertical or horizontal
    if(dx == 0 and dy >= 1) or (dx >=1 and dy == 0):

        #direction of movement
        if dx == 0: #moving vertically
            step_x = 0
            step_y = 1 if end_y > start_y else -1
        else: #moving horizontally
            step_x = 1 if end_x > start_x else -1
            step_y = 0
        

        #check if path is clear
        x, y = start_x + step_x, start_y + step_y
        while x != end_x and y != end_y:
            if (x, y) in pieces:
                return False
            x += step_x
            y += step_y
        
        #check if empty or has opponent's piece
        if(end_x, end_y) not in pieces or pieces[(end_x - end_y)].color != piece.color:
            return True
        
    return False

def is_valid_queen_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    #check diagonal, vertical and horizontal movement "patterns"
    if (dx == dy) or (dx == 0 and dy >= 1) or (dx >=1 and dy == 0):
        #check for pieces in the way
        if dx == dy: #diagonal movement
            step_x = 1 if end_x > start_x else -1
            step_y = 1 if end_y > start_y else -1
        elif dx == 0: #vertical movement
            step_x = 0
            step_y = 1 if end_y > start_y else -1
        else: #horizontal movement
            step_x = 1 if end_x > start_x else -1
            step_y = 0
        
         # Check if the path is clear
        x, y = start_x + step_x, start_y + step_y
        while x != end_x or y != end_y:
            if (x, y) in pieces:
                return False
            x += step_x
            y += step_y
        

        # Check if the destination square is empty or contains an opponent's piece
        if (end_x, end_y) not in pieces or pieces[(end_x, end_y)].color != piece.color:
            return True

    return False

def is_valid_king_move(piece, new_position, pieces):
    start_x, start_y = piece.position
    end_x, end_y = new_position

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    #king can move in any direction one square
    if max(dx, dy) == 1: #max() returns the highest value. So as long as dx, or dy is not >1
        #check for empty or opponent's pieces
        if(end_x, end_y) not in pieces or pieces[(end_x - end_y)].color != piece.color:
            return True
    return False



#funciton to draw the board
def draw_board():
    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, color_dark_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            else:
                pygame.draw.rect(surface, color_light_green, pygame.Rect(x * square_size, y * square_size, square_size, square_size))

#dictionary with Piece class
pieces = {
    (0, 1): Piece("Pieces Images/pawn-b.svg", (0, 1), square_size, offset, "pawn", 'b'),
    (1, 1): Piece("Pieces Images/pawn-b.svg", (1, 1), square_size, offset, "pawn", 'b'),
    (2, 1): Piece("Pieces Images/pawn-b.svg", (2, 1), square_size, offset, "pawn", 'b'),
    (3, 1): Piece("Pieces Images/pawn-b.svg", (3, 1), square_size, offset, "pawn", 'b'),
    (4, 1): Piece("Pieces Images/pawn-b.svg", (4, 1), square_size, offset, "pawn", 'b'),
    (5, 1): Piece("Pieces Images/pawn-b.svg", (5, 1), square_size, offset, "pawn", 'b'),
    (6, 1): Piece("Pieces Images/pawn-b.svg", (6, 1), square_size, offset, "pawn", 'b'),
    (7, 1): Piece("Pieces Images/pawn-b.svg", (7, 1), square_size, offset, "pawn", 'b'),

    (0, 6): Piece("Pieces Images/pawn-w.svg", (0, 6), square_size, offset, "pawn", 'w'),
    (1, 6): Piece("Pieces Images/pawn-w.svg", (1, 6), square_size, offset, "pawn", 'w'),
    (2, 6): Piece("Pieces Images/pawn-w.svg", (2, 6), square_size, offset, "pawn", 'w'),
    (3, 6): Piece("Pieces Images/pawn-w.svg", (3, 6), square_size, offset, "pawn", 'w'),
    (4, 6): Piece("Pieces Images/pawn-w.svg", (4, 6), square_size, offset, "pawn", 'w'),
    (5, 6): Piece("Pieces Images/pawn-w.svg", (5, 6), square_size, offset, "pawn", 'w'),
    (6, 6): Piece("Pieces Images/pawn-w.svg", (6, 6), square_size, offset, "pawn", 'w'),
    (7, 6): Piece("Pieces Images/pawn-w.svg", (7, 6), square_size, offset, "pawn", 'w'),

    (1, 0): Piece("Pieces Images/knight-b.svg", (1, 0), square_size, offset, "knight", 'b'),
    (6, 0): Piece("Pieces Images/knight-b.svg", (6, 0), square_size, offset, "knight", 'b'),

    (1, 7): Piece("Pieces Images/knight-w.svg", (1, 7), square_size, offset, "knight", 'w'),
    (6, 7): Piece("Pieces Images/knight-w.svg", (6, 7), square_size, offset, "knight", 'w'),

    (2, 0): Piece("Pieces Images/bishop-b.svg", (2, 0), square_size, offset, "bishop", 'b'),
    (5, 0): Piece("Pieces Images/bishop-b.svg", (5, 0), square_size, offset, "bishop", 'b'),

    (2, 7): Piece("Pieces Images/bishop-w.svg", (2, 7), square_size, offset, "bishop", 'w'),
    (5, 7): Piece("Pieces Images/bishop-w.svg", (5, 7), square_size, offset, "bishop", 'w'),

    (0, 0): Piece("Pieces Images/rook-b.svg", (0, 0), square_size, offset, "rook", 'b'),
    (7, 0): Piece("Pieces Images/rook-b.svg", (7, 0), square_size, offset, "rook", 'b'),

    (0, 7): Piece("Pieces Images/rook-w.svg", (0, 7), square_size, offset, "rook", 'w'),
    (7, 7): Piece("Pieces Images/rook-w.svg", (7, 7), square_size, offset, "rook", 'w'),

    (3, 0): Piece("Pieces Images/queen-b.svg", (3, 0), square_size, offset, "queen", 'b'),
    (3, 7): Piece("Pieces Images/queen-w.svg", (3, 7), square_size, offset, "queen", 'w'),

    (4, 0): Piece("Pieces Images/king-b.svg", (4, 0), square_size, offset, "king", 'b'),
    (4, 7): Piece("Pieces Images/king-w.svg", (4, 7), square_size, offset, "king", 'w')
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
                mx, my = pygame.mouse.get_pos()
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

                if dragging_piece.piece_type == 'pawn' and is_valid_pawn_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                elif dragging_piece.piece_type == 'knight' and is_valid_knight_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                elif dragging_piece.piece_type == 'bishop' and is_valid_bishop_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                elif dragging_piece.piece_type == 'rook' and is_valid_rook_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                elif dragging_piece.piece_type == 'queen' and is_valid_queen_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                elif dragging_piece.piece_type == 'king' and is_valid_queen_move(dragging_piece, new_position, pieces):
                    pieces.pop(dragging_piece.position)
                    dragging_piece.move(new_position)
                    pieces[new_position] = dragging_piece
                else:
                    # Reset the position of the piece if move is invalid
                    dragging_piece.move(dragging_piece.position)

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
