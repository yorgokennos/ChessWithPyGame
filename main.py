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
        self.image = pygame.transform.scale(self.image, (square_size - 2 * offset, square_size - 2 * offset)) 
        #DEBUGGING
        print(f"Scaled image size: {self.image.get_width()} x {self.image.get_height()}")
        #DEBUGGING
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
        if(end_x, end_y) not in pieces or pieces[(end_x, end_y)].color != piece.color:
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
        if(end_x, end_y) not in pieces or pieces[(end_x, end_y)].color != piece.color:
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
        if(end_x, end_y) not in pieces or pieces[(end_x, end_y)].color != piece.color:
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


def is_in_check(color, pieces):
    #Find the king
    king_position = None

    for piece in pieces.values():
        if piece.piece_type == "king" and piece.color == color:
            king_position = piece.position
            break
    
    #check if any pieces can attach the king
    for piece in pieces.values():
        if piece.color != color:
            if piece.piece_type == "pawn" and is_valid_pawn_move(piece, king_position, pieces):
                return True
            if piece.piece_type == "knight" and is_valid_knight_move(piece, king_position, pieces):
                return True
            if piece.piece_type == "bishop" and is_valid_bishop_move(piece, king_position, pieces):
                return True
            if piece.piece_type == "rook" and is_valid_rook_move(piece, king_position, pieces):
                return True
            if piece.piece_type == "queen" and is_valid_queen_move(piece, king_position, pieces):
                return True
            if piece.piece_type == "king" and is_valid_king_move(piece, king_position, pieces):
                return True

    return False

def is_checkmate(color, pieces):
    for piece in pieces.values():
            if piece.color == color:
                original_position = piece.position
                for x in range(8):
                    for y in range(8):
                        new_position = (x, y)
                        if piece.piece_type == "pawn" and is_valid_pawn_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
                        if piece.piece_type == "knight" and is_valid_knight_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
                        if piece.piece_type == "bishop" and is_valid_bishop_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
                        if piece.piece_type == "rook" and is_valid_rook_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
                        if piece.piece_type == "queen" and is_valid_queen_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
                        if piece.piece_type == "king" and is_valid_king_move(piece, new_position, pieces):
                            if try_move(piece, new_position, pieces, color):
                                return False
    return True

def try_move(piece, new_position, pieces, color):
    original_position = piece.position
    original_piece_at_dest = pieces.get(new_position)
    pieces[new_position] = piece
    del pieces[original_position]
    piece.position = new_position

    in_check = is_in_check(color, pieces)

    piece.position = original_position
    pieces[original_position] = piece
    if original_piece_at_dest:
        pieces[new_position] = original_piece_at_dest
    else:
        del pieces[new_position]

    return not in_check

def is_stalemate(color, pieces):
    if is_in_check(color, pieces):
        return False
    
    for piece in pieces.values():
        if piece.color == color:
            original_position = piece.position
            for x in range(8):
                for y in range(8):
                    new_position = (x, y)
                    if piece.piece_type == "pawn" and is_valid_pawn_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
                    if piece.piece_type == "knight" and is_valid_knight_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
                    if piece.piece_type == "bishop" and is_valid_bishop_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
                    if piece.piece_type == "rook" and is_valid_rook_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
                    if piece.piece_type == "queen" and is_valid_queen_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
                    if piece.piece_type == "king" and is_valid_king_move(piece, new_position, pieces):
                        if try_move(piece, new_position, pieces, color):
                            return False
    return True


def can_castle(kingside, color, pieces):
    if kingside:
        rook_pos = (7, 0) if color == 'w' else (7, 7)
        squares_between = [(5, 0), (6, 0)] if color == 'w' else [(5, 7), (6, 7)]
    else:
        rook_pos = (0, 0) if color == 'w' else (0, 7)
        squares_between = [(1, 0), (2, 0), (3, 0)] if color == 'w' else [(1, 7), (2, 7), (3, 7)]

    king_pos = (4, 0) if color == 'w' else (4, 7)
    king = pieces.get(king_pos)
    rook = pieces.get(rook_pos)

    if not king or not rook or king.moved or rook.moved:
        return False

    for square in squares_between:
        if square in pieces or is_in_check(color, pieces):
            return False

    # Ensure the king doesn't pass through check
    for i in range(min(king_pos[0], rook_pos[0]), max(king_pos[0], rook_pos[0]) + 1):
        if is_in_check(color, pieces):
            return False

    return True

def perform_castle(kingside, color, pieces):
    if can_castle(kingside, color, pieces):
        if kingside:
            rook_pos = (7, 0) if color == 'w' else (7, 7)
            new_king_pos = (6, 0) if color == 'w' else (6, 7)
            new_rook_pos = (5, 0) if color == 'w' else (5, 7)
        else:
            rook_pos = (0, 0) if color == 'w' else (0, 7)
            new_king_pos = (2, 0) if color == 'w' else (2, 7)
            new_rook_pos = (3, 0) if color == 'w' else (3, 7)

        king_pos = (4, 0) if color == 'w' else (4, 7)
        king = pieces[king_pos]
        rook = pieces[rook_pos]

        del pieces[king_pos]
        del pieces[rook_pos]

        king.position = new_king_pos
        rook.position = new_rook_pos

        pieces[new_king_pos] = king
        pieces[new_rook_pos] = rook
        king.moved = True
        rook.moved = True



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
    (0, 1): Piece(r"Pieces Images\NEW\bp.png", (0, 1), square_size, offset, "pawn", 'b'),
    (1, 1): Piece(r"Pieces Images\NEW\bp.png", (1, 1), square_size, offset, "pawn", 'b'),
    (2, 1): Piece(r"Pieces Images\NEW\bp.png", (2, 1), square_size, offset, "pawn", 'b'),
    (3, 1): Piece(r"Pieces Images\NEW\bp.png", (3, 1), square_size, offset, "pawn", 'b'),
    (4, 1): Piece(r"Pieces Images\NEW\bp.png", (4, 1), square_size, offset, "pawn", 'b'),
    (5, 1): Piece(r"Pieces Images\NEW\bp.png", (5, 1), square_size, offset, "pawn", 'b'),
    (6, 1): Piece(r"Pieces Images\NEW\bp.png", (6, 1), square_size, offset, "pawn", 'b'),
    (7, 1): Piece(r"Pieces Images\NEW\bp.png", (7, 1), square_size, offset, "pawn", 'b'),
    (0, 6): Piece(r"Pieces Images\NEW\wp.png", (0, 6), square_size, offset, "pawn", 'w'),
    (1, 6): Piece(r"Pieces Images\NEW\wp.png", (1, 6), square_size, offset, "pawn", 'w'),
    (2, 6): Piece(r"Pieces Images\NEW\wp.png", (2, 6), square_size, offset, "pawn", 'w'),
    (3, 6): Piece(r"Pieces Images\NEW\wp.png", (3, 6), square_size, offset, "pawn", 'w'),
    (4, 6): Piece(r"Pieces Images\NEW\wp.png", (4, 6), square_size, offset, "pawn", 'w'),
    (5, 6): Piece(r"Pieces Images\NEW\wp.png", (5, 6), square_size, offset, "pawn", 'w'),
    (6, 6): Piece(r"Pieces Images\NEW\wp.png", (6, 6), square_size, offset, "pawn", 'w'),
    (7, 6): Piece(r"Pieces Images\NEW\wp.png", (7, 6), square_size, offset, "pawn", 'w'),
    (1, 0): Piece(r"Pieces Images\NEW\bn.png", (1, 0), square_size, offset, "knight", 'b'),
    (6, 0): Piece(r"Pieces Images\NEW\bn.png", (6, 0), square_size, offset, "knight", 'b'),
    (1, 7): Piece(r"Pieces Images\NEW\wn.png", (1, 7), square_size, offset, "knight", 'w'),
    (6, 7): Piece(r"Pieces Images\NEW\wn.png", (6, 7), square_size, offset, "knight", 'w'),
    (2, 0): Piece(r"Pieces Images\NEW\bb.png", (2, 0), square_size, offset, "bishop", 'b'),
    (5, 0): Piece(r"Pieces Images\NEW\bb.png", (5, 0), square_size, offset, "bishop", 'b'),
    (2, 7): Piece(r"Pieces Images\NEW\wb.png", (2, 7), square_size, offset, "bishop", 'w'),
    (5, 7): Piece(r"Pieces Images\NEW\wb.png", (5, 7), square_size, offset, "bishop", 'w'),
    (0, 0): Piece(r"Pieces Images\NEW\br.png", (0, 0), square_size, offset, "rook", 'b'),
    (7, 0): Piece(r"Pieces Images\NEW\br.png", (7, 0), square_size, offset, "rook", 'b'),
    (0, 7): Piece(r"Pieces Images\NEW\wr.png", (0, 7), square_size, offset, "rook", 'w'),
    (7, 7): Piece(r"Pieces Images\NEW\wr.png", (7, 7), square_size, offset, "rook", 'w'),
    (3, 0): Piece(r"Pieces Images\NEW\bq.png", (3, 0), square_size, offset, "queen", 'b'),
    (3, 7): Piece(r"Pieces Images\NEW\wq.png", (3, 7), square_size, offset, "queen", 'w'),
    (4, 0): Piece(r"Pieces Images\NEW\bk.png", (4, 0), square_size, offset, "king", 'b'),
    (4, 7): Piece(r"Pieces Images\NEW\wk.png", (4, 7), square_size, offset, "king", 'w')
}

dragging_piece = None
dragging_offset_x = 0
dragging_offset_y = 0

# Variable to track the current player's turn
current_turn = 'w'  # Start with white player

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces.values():
                if piece.rect.collidepoint(event.pos):
                    if piece.color == current_turn:  # Check if it's the current player's turn
                        dragging_piece = piece
                        mouse_x, mouse_y = event.pos
                        dragging_offset_x = piece.rect.x - mouse_x
                        dragging_offset_y = piece.rect.y - mouse_y
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_piece is not None:
                mouse_x, mouse_y = event.pos
                new_position = (mouse_x // square_size, mouse_y // square_size)

                valid_move = False
                if dragging_piece.piece_type == "pawn":
                    valid_move = is_valid_pawn_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "knight":
                    valid_move = is_valid_knight_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "bishop":
                    valid_move = is_valid_bishop_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "rook":
                    valid_move = is_valid_rook_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "queen":
                    valid_move = is_valid_queen_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "king":
                    valid_move = is_valid_king_move(dragging_piece, new_position, pieces)
                elif dragging_piece.piece_type == "king_castle":
                    if can_castle(True, dragging_piece.color, pieces):
                        perform_castle(True, dragging_piece.color, pieces)
                        current_turn = 'b' if current_turn == 'w' else 'w'
                        dragging_piece = None
                        continue
                    else:
                        valid_move = False
                elif dragging_piece.piece_type == "queen_castle":
                    if can_castle(False, dragging_piece.color, pieces):
                        perform_castle(False, dragging_piece.color, pieces)
                        current_turn = 'b' if current_turn == 'w' else 'w'
                        dragging_piece = None
                        continue
                    else:
                        valid_move = False

                if valid_move:
                    if new_position in pieces:
                        if pieces[new_position].color != dragging_piece.color:
                            del pieces[new_position]  # Capture the piece
                        else:
                            valid_move = False  # Invalid move, can't capture own piece

                    if valid_move:
                        original_position = dragging_piece.position
                        del pieces[original_position]
                        dragging_piece.move(new_position)
                        pieces[new_position] = dragging_piece

                        # Check for check and checkmate
                        opponent_color = 'b' if dragging_piece.color == 'w' else 'w'
                        if is_in_check(opponent_color, pieces):
                            if is_checkmate(opponent_color, pieces):
                                print(f"Checkmate! {dragging_piece.color} wins!")
                                running = False
                        elif is_stalemate(opponent_color, pieces):
                            print("Stalemate!")
                            running = False

                        # Switch turns after a valid move
                        current_turn = 'b' if current_turn == 'w' else 'w'
                    else:
                        dragging_piece.move(dragging_piece.position)  # Snapback to original position
                else:
                    dragging_piece.move(dragging_piece.position)  # Snapback to original position

                dragging_piece = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_piece is not None:
                mouse_x, mouse_y = event.pos
                dragging_piece.rect.x = mouse_x + dragging_offset_x
                dragging_piece.rect.y = mouse_y + dragging_offset_y

    draw_board()
    for piece in pieces.values():
        piece.draw(surface)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
