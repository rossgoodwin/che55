def position(square):
    # converts algebraic notation (e.g. "e4") into coordinates
    square = list(square)
    global files
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    global ranks
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    x = files.index(square[0]) * 80 + 70
    y = 630 - ranks.index(square[1]) * 80
    return (x, y)

def square(position):
    # converts coordinates into algebraic notation
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

class Pawn(Piece):
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
            
class King(Piece):
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
        

def moveviz(m):
    pos1 = position(m[0]+m[1])
    pos2 = position(m[2]+m[3])
    return [pos1[0], pos1[1], pos2[0], pos2[1]]

def mousePressed():
    if 30 < mouseX < 670 and 30 < mouseY < 670:
        global selected
        mouseSquare = square((mouseX, mouseY))
        for p in pieces:
            if square(p.currentPos) == mouseSquare:
                selected = p
            else:
                pass
        global mousebutt
        mousebutt = True

def mouseReleased():
    if 30 < mouseX < 670 and 30 < mouseY < 670:
        global mousebutt
        mousebutt = False
        mouseSquare = square((mouseX, mouseY))
        global selected
        selected.currentPos = position(mouseSquare)
        global pieces
        for p in pieces:
            if p != selected and p.currentPos == selected.currentPos:
                global captured
                captured = p
                if captured.side == 1:
                    global whiteCapturedCount
                    whiteCapturedCount += 1
                    captured.currentPos = (700+30*whiteCapturedCount, 70)
                    captured = Piece('e5', 1)
                else:
                    global blackCapturedCount
                    blackCapturedCount += 1
                    captured.currentPos = (700+30*blackCapturedCount, 630)
                    captured = Piece('e5', 1)
        selected = Piece('e4', 1)

def setup():
    size(displayWidth, displayHeight)
    
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
    
    global whiteCapturedCount
    whiteCapturedCount = 0
    
    global blackCapturedCount
    blackCapturedCount = 0
    
    global mousebutt
    mousebutt = False
    
def draw():
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
    
    # to ensure selected piece stays on top
    if mousebutt:
        selected.display()
