def position(square):
    # converts algebraic notation (e.g. "e4") into coordinates
    square = list(square)
    global files
    global ranks
    x = files.index(square[0]) * 80 + 70
    y = 630 - ranks.index(square[1]) * 80
    return (x, y)

def square(position):
    # converts coordinates into algebraic notation
    global files
    global ranks
    file_index = (position[0] - 30) / 80
    rank_index = (670 - position[1]) / 80
    if 30 < position[0] < 670 and 30 < position[1] < 670:
        s = files[file_index] + ranks[rank_index]
    else:
        s = None
    return s

class Piece(object):
    # initialize attributes
    def __init__(self, startSq, side):
        self.startSq = startSq
        self.startPos = position(startSq)
        self.currentPos = self.startPos
        self.side = side
        self.beenCaptured = False

class Pawn(Piece):
    # TODO: 1. ENPASSANT
    # 2. BECOMING A QUEEN (OR ANY OTHER PIECE)
    def display(self):
    # display at currentPos
        self.shadow()
        if self.side == 1:
            stroke(137)
            fill(255)
        else:
            stroke(137)
            fill(0)
        smooth()
        ellipseMode(CENTER)
        ellipse(self.currentPos[0], self.currentPos[1], 20, 20)
    def shadow(self):
        smooth()
        noStroke()
        fill(50, 50)
        ellipseMode(CENTER)
        global selected
        if selected == self:
            ellipse(self.currentPos[0], self.currentPos[1]+7, 20, 20)
        else:
            ellipse(self.currentPos[0], self.currentPos[1]+4, 20, 20)
            
    def legalmove(self, move):
        # TODO: NEED TO ADD RULES FOR ENPASSANT
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
        
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        global pieces
        global enpassantOp
        global enpassantable
        
        if horizontalDiff == 0 and (verticalDiff == -1 + self.side * 2):
            legal = True
            for p in pieces:
                if p != self and square(p.currentPos) == destSq:
                    legal = False
        elif horizontalDiff == 0 and (verticalDiff == -2 + self.side * 4) and originSq == self.startSq:
            legal = True
            for p in pieces:
                if p != self and (square(p.currentPos) == destSq or square(p.currentPos) == destSq[0] + str(int(destSq[1]) + 1 + self.side * -2)):
                    legal = False
        elif abs(horizontalDiff) == 1 and (verticalDiff == -1 + self.side * 2):
            for p in pieces:
                if p != self and p.side != self.side and square(p.currentPos) == destSq:
                    legal = True
                elif enpassantOp and p == enpassantable and p.side != self.side and pieces.index(p) < 16 and p.beenCaptured == False and square(p.currentPos) == destSq[0] + str(int(destSq[1]) + 1 + self.side * -2):
                    legal = True
        return legal
        
class Bishop(Piece):
    def display(self):
        self.shadow()
        smooth()
        if self.side == 1:
            stroke(137)
            fill(255)
        else:
            stroke(137)
            fill(0)
        triangle(self.currentPos[0], self.currentPos[1]-10*sqrt(2),
                self.currentPos[0]+20, self.currentPos[1]+10*sqrt(2),
                self.currentPos[0]-20, self.currentPos[1]+10*sqrt(2))
    def shadow(self):
        smooth()
        noStroke()
        fill(50, 50)
        if selected == self:
            triangle(self.currentPos[0], self.currentPos[1]-10*sqrt(2)+7,
                     self.currentPos[0]+20, self.currentPos[1]+10*sqrt(2)+7,
                     self.currentPos[0]-20, self.currentPos[1]+10*sqrt(2)+7)
        else:
            triangle(self.currentPos[0], self.currentPos[1]-10*sqrt(2)+4,
                     self.currentPos[0]+20, self.currentPos[1]+10*sqrt(2)+4,
                     self.currentPos[0]-20, self.currentPos[1]+10*sqrt(2)+4)
    
    def legalmove(self, move):
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
        
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        global pieces
        if abs(horizontalDiff) == abs(verticalDiff) and horizontalDiff != 0:
        # if move == diagonal
            legal = True
            # but if there are pieces in the way...
            if horizontalDiff > 0 and verticalDiff > 0:
            # file+, rank+
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
            elif horizontalDiff < 0 and verticalDiff < 0:
            # file-, rank-
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff > 0 and verticalDiff < 0:
            # file+, rank-
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff < 0 and verticalDiff > 0:
            # file-, rank+
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
        
        # prevent taking own pieces
        for p in pieces:
            if p != self and square(p.currentPos) == destSq and self.side == p.side:
                legal = False
        
        return legal
            

class Knight(Piece):
    def display(self):
        self.shadow()
        smooth()
        if self.side == 1:
            stroke(137)
            fill(255)
        else:
            stroke(137)
            fill(0)
        ellipseMode(CENTER)
        arc(self.currentPos[0]-12.5, self.currentPos[1]+20, 50, 80, PI+HALF_PI, TWO_PI, PIE)
    def shadow(self):
        smooth()
        noStroke()
        fill(50, 50)
        ellipseMode(CENTER)
        if selected == self:
            arc(self.currentPos[0]-12.5, self.currentPos[1]+20+7, 50, 80, PI+HALF_PI, TWO_PI, PIE)
        else:
            arc(self.currentPos[0]-12.5, self.currentPos[1]+20+4, 50, 80, PI+HALF_PI, TWO_PI, PIE)
            
    def legalmove(self, move):
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
  
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        if (abs(verticalDiff) == 2 and abs(horizontalDiff) == 1) or (abs(verticalDiff) == 1 and abs(horizontalDiff) == 2):
            legal = True
        
        # prevent taking own pieces
        for p in pieces:
            if p != self and square(p.currentPos) == destSq and self.side == p.side:
                legal = False
        
        return legal
            

class Rook(Piece):
    def display(self):
        self.shadow()
        smooth()
        if self.side == 1:
            stroke(137)
            fill(255)
        else:
            stroke(137)
            fill(0)
        rectMode(CENTER)
        rect(self.currentPos[0], self.currentPos[1], 25, 25)
    def shadow(self):
        smooth()
        noStroke()
        fill(50, 50)
        rectMode(CENTER)
        if selected == self:
            rect(self.currentPos[0], self.currentPos[1]+7, 25, 25)
        else:
            rect(self.currentPos[0], self.currentPos[1]+4, 25, 25)    
    
    def legalmove(self, move):
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
  
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        if (horizontalDiff != 0 and verticalDiff == 0) or (horizontalDiff == 0 and verticalDiff != 0):
            legal = True
            if verticalDiff > 0:
                for i in range(1, verticalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == destSq[0] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
            elif verticalDiff < 0:
                for i in range(1, abs(verticalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == destSq[0] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff > 0:
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + destSq[1]):
                            legal = False
            elif horizontalDiff < 0:
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + destSq[1]):
                            legal = False
        
        # prevent taking own pieces
        for p in pieces:
            if p != self and square(p.currentPos) == destSq and self.side == p.side:
                legal = False
        
        return legal
                
        
class Queen(Piece):
    def display(self):
        self.shadow()
        global whiteQueen
        whiteQueen = loadShape("whitequeen.svg")
        global blackQueen
        blackQueen = loadShape("blackqueen.svg")
        shapeMode(CENTER)
        smooth()
        if self.side == 1:
            shape(whiteQueen, self.currentPos[0], self.currentPos[1], 50, 50)
        else:
            shape(blackQueen, self.currentPos[0], self.currentPos[1], 50, 50)
    def shadow(self):
        global queenShadow
        queenShadow = loadShape("queenshadow.svg")
        shapeMode(CENTER)
        smooth()
        if selected == self:
            shape(queenShadow, self.currentPos[0], self.currentPos[1]+7, 50, 50)
        else:
            shape(queenShadow, self.currentPos[0], self.currentPos[1]+4, 50, 50)    
    
    def legalmove(self, move):
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
  
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        # rook logic + bishop logic
        # TODO: MAKE THESE FUNCTIONS BECAUSE D.R.Y.
        if (horizontalDiff != 0 and verticalDiff == 0) or (horizontalDiff == 0 and verticalDiff != 0):
            legal = True
            if verticalDiff > 0:
                for i in range(1, verticalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == destSq[0] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
            elif verticalDiff < 0:
                for i in range(1, abs(verticalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == destSq[0] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff > 0:
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + destSq[1]):
                            legal = False
            elif horizontalDiff < 0:
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + destSq[1]):
                            legal = False
        elif abs(horizontalDiff) == abs(verticalDiff) and horizontalDiff != 0:
        # if move == diagonal
            legal = True
            # but if there are pieces in the way...
            if horizontalDiff > 0 and verticalDiff > 0:
            # file+, rank+
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
            elif horizontalDiff < 0 and verticalDiff < 0:
            # file-, rank-
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff > 0 and verticalDiff < 0:
            # file+, rank-
                for i in range(1, horizontalDiff):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])-i] + ranks[ranks.index(destSq[1])+i]):
                            legal = False
            elif horizontalDiff < 0 and verticalDiff > 0:
            # file-, rank+
                for i in range(1, abs(horizontalDiff)):
                    for p in pieces:
                        if p != self and (square(p.currentPos) == files[files.index(destSq[0])+i] + ranks[ranks.index(destSq[1])-i]):
                            legal = False
                            
        # prevent taking own pieces
        for p in pieces:
            if p != self and square(p.currentPos) == destSq and self.side == p.side:
                legal = False
        
        return legal
    
            
class King(Piece):
    # TODO: [X] MOVING INTO / OUT OF CHECK
    # [ ] CASTLING
    def display(self):
        self.shadow()
        smooth()
        if self.side == 1:
            stroke(137)
            fill(255)
        else:
            stroke(137)
            fill(0)
        rectMode(CENTER)
        rect(self.currentPos[0], self.currentPos[1], 40, 10)
        rect(self.currentPos[0], self.currentPos[1], 10, 40)
        noStroke()
        rect(self.currentPos[0], self.currentPos[1], 15, 8)
    def shadow(self):
        smooth()
        noStroke()
        fill(50, 50)
        rectMode(CENTER)
        if selected == self:
            rect(self.currentPos[0], self.currentPos[1]+7, 40, 10)
            rect(self.currentPos[0], self.currentPos[1]+7, 10, 40)
        else:
            rect(self.currentPos[0], self.currentPos[1]+4, 40, 10)
            rect(self.currentPos[0], self.currentPos[1]+4, 10, 40)
            
    def legalmove(self, move):
        move = list(move)
        originSq = move[0]+move[1]
        destSq = move[2]+move[3]
        legal = False
  
        global files
        global ranks
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        
        if (abs(horizontalDiff) == 1 and verticalDiff == 0) or (abs(verticalDiff) == 1 and horizontalDiff == 0) or (abs(verticalDiff) == 1 and abs(horizontalDiff) == 1):
            legal = True
            for p in pieces:
                if p != self and square(p.currentPos) == destSq and self.side == p.side:
                    legal = False
        
        return legal
        

def moveviz(m):
    pos1 = position(m[0]+m[1])
    pos2 = position(m[2]+m[3])
    return [pos1[0], pos1[1], pos2[0], pos2[1]]


def selfCheck():
    legal = True
    global game
    global pieces
    whiteKingPos = square(pieces[30].currentPos)
    blackKingPos = square(pieces[31].currentPos)
    if len(game) % 2 == 0:
        for p in pieces[:30]:
            if not p.beenCaptured and p.legalmove(square(p.currentPos)+whiteKingPos):
                legal = False
    else:
        for p in pieces[:30]:
            if not p.beenCaptured and p.legalmove(square(p.currentPos)+blackKingPos):
                legal = False
    return legal

def enpassant():
    global enpassantOp
    global game
    global pieces
    global enpassantable
    enpassantOp = False
    enpassantable = None
    if len(game) > 0:
        priorMove = list(game[-1])
        originSq = priorMove[0]+priorMove[1]
        destSq = priorMove[2]+priorMove[3]
        horizontalDiff = files.index(destSq[0]) - files.index(originSq[0])
        verticalDiff = ranks.index(destSq[1]) - ranks.index(originSq[1])
        for p in pieces[:16]:
            if square(p.currentPos) == destSq and p.startSq == originSq and horizontalDiff == 0 and abs(verticalDiff) == 2:
                enpassantOp = True
                enpassantable = p
                
def mousePressed():
    if 30 < mouseX < 670 and 30 < mouseY < 670:
        global selected
        global lastMoveOriginSquare
        global game
        global mousebutt
        mouseSquare = square((mouseX, mouseY))
        for p in pieces:
            if square(p.currentPos) == mouseSquare and len(game) % 2 != p.side:
                selected = p
                lastMoveOriginSquare = square(p.currentPos)
                mousebutt = True
            else:
                pass

def mouseReleased():
    global mousebutt
    if 30 < mouseX < 670 and 30 < mouseY < 670 and mousebutt == True:
        enpassant()
        mousebutt = False
        mouseSquare = square((mouseX, mouseY))
        global lastmove
        lastmove = lastMoveOriginSquare+mouseSquare
        global selected
        global enpassantOp
        global enpassantable
        if selected.legalmove(lastmove):
            global pieces
            global captured
            for p in pieces:
                if (p.side != selected.side and square(p.currentPos) == square(selected.currentPos)) or \
                   (enpassantOp and p == enpassantable and pieces.index(p) < 16 and p.side != selected.side and square(p.currentPos) == square(selected.currentPos)[0] + str(int(square(selected.currentPos)[1])-1+p.side*2)):
                    captured = p
                    captured.beenCaptured = True
                    if captured.side == 1 and selfCheck():
                        global whiteCapturedCount
                        whiteCapturedCount +=1
                        captured.currentPos = (700+30*whiteCapturedCount, 70)
                        captured = Piece('e5', 1)
                    elif captured.side == 0 and selfCheck():
                        global blackCapturedCount
                        blackCapturedCount += 1
                        captured.currentPos = (700+30*blackCapturedCount, 630)
                        captured = Piece('e5', 1)
                    else:
                        captured.beenCaptured = False
                        captured = Piece('e5', 1)
            if selfCheck():
                selected.currentPos = position(mouseSquare)
                global game
                game.append(lastmove)
                print game
            else:
                selected.currentPos = position(lastMoveOriginSquare)
        else:
            selected.currentPos = position(lastMoveOriginSquare)
        selected = Piece('e4', 1)
        enpassantOp = False
        enpassantable = None
        
def setup():
    # TODO: PLAY AS BLACK
    # TODO: ANIMATED ENGINE MOVES
    # [X] TODO: IMPLEMENT GAME LIST
    # THINGS THAT GO WITH GAME LIST:
    # [X] TURNS (ONLY SIDE THAT HAS TURN CAN MOVE)
    # [X] CAN'T MOVE INTO CHECK
    # - CASTLING
    #    - NO CASTLING THROUGH CHECK
    #    - NO CASTLING THROUGH PIECES
    #    - NO CASTLING OUT OF CHECK
    #    - NO CASTLING AFTER KING OR ROOK HAS MOVED
    # [X] ENPASSANT
    # - PAWNS BECOMING QUEENS, ETC.
    # [X] CHECK
    # - CHECKMATE
    size(displayWidth, displayHeight)
    
    global whiteCapturedCount
    whiteCapturedCount = 0
    
    global blackCapturedCount
    blackCapturedCount = 0
    
    global mousebutt
    mousebutt = False
    
    global lastMoveOriginSquare
    lastMoveOriginSquare = None
    
    global enpassantOp
    enpassantOp = False
    
    global game
    game = []
    
    global files
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    files.reverse()
    global ranks
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    ranks.reverse()
    
    # create fonts
    global josefin
    josefin = createFont("JosefinSans-Regular", 16)
    
    # instantiate pieces
    whitePawnStartPos = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
    blackPawnStartPos = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
    whitePawns = [Pawn(p, 1) for p in whitePawnStartPos]
    blackPawns = [Pawn(p, 0) for p in blackPawnStartPos]
    bishops = [Bishop('c1', 1), Bishop('f1', 1), Bishop('c8', 0), Bishop('f8', 0)]
    knights = [Knight('b1', 1), Knight('g1', 1), Knight('b8', 0), Knight('g8', 0)]
    rooks = [Rook('a1', 1), Rook('h1', 1), Rook('a8', 0), Rook('h8', 0)]
    queens = [Queen('d1', 1), Queen('d8', 0)]
    kings = [King('e1', 1), King('e8', 0)]
    
    # make global pieces list
    global pieces
    pieces = whitePawns + blackPawns + bishops + knights + rooks + queens + kings
    
    global selected
    selected = Piece('e4', 1)
    
    global captured
    captured = Piece('e5', 1)
    
    global enpassantable
    enpassantable = None
    
def draw():
    # TODO: IMPLMENENT ANIMATED ENGINE MOVES
    # draw the background
    background(230)
    
    # draw the board frame
    noStroke()
    fill(188, 154, 105)
    triangle(10, 10, 690, 10, 350, 350)
    fill(127, 104, 71)
    triangle(10, 690, 350, 350, 690, 690)
    fill(156, 129, 86)
    triangle(10, 10, 350, 350, 10, 690)
    triangle(690, 10, 350, 350, 690, 690)
    
    # draw the board grid
    noStroke()
    for i in range(8):
        for j in range(8):
            if (i%2==1 and j%2==0) or (i%2==0 and j%2==1):
                fill(84, 167, 87)
            else:
                fill(243, 240, 213)
            rectMode(CORNER)
            rect(30+i*80, 30+j*80, 80, 80)
            
    # draw the coordinate labels
    textFont(josefin)
    fill(233, 233, 234)
    for i in range(8):
        textAlign(CENTER, TOP)
        text(files[i].upper(), 70+80*i, 670)
        textAlign(RIGHT, CENTER)
        text(ranks[7-i], 25, 70+80*i)
    
    # while mouse pressed, and until mouse released,
    # selected piece follows cursor
    global mousebutt
    global selected
    if mousebutt:
        selected.currentPos = (mouseX, mouseY)
    
    # display pieces
    global pieces
    for p in pieces:
        p.display()
    
    # ensure selected piece stays on top
    if mousebutt:
        selected.display()
