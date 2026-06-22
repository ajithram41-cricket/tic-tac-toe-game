"""
Tic Tac Toe — Modern Pygame Edition
Features: 2-Player & vs AI, 3 difficulty levels, match history, animated UI
"""

import pygame
import sys
import random
import math

pygame.init()

W, H        = 720, 820
FPS         = 60
BOARD_TOP   = 265
BOARD_SIZE  = 360
CELL        = BOARD_SIZE // 3
BOARD_LEFT  = (W - BOARD_SIZE) // 2

BG          = (248, 248, 250)
SURFACE     = (255, 255, 255)
BORDER      = (220, 220, 225)
TEXT_PRI    = (28,  28,  32)
TEXT_SEC    = (110, 110, 120)
TEXT_HINT   = (170, 170, 180)

X_FILL      = (230, 241, 251)
X_BORDER    = (133, 183, 235)
X_COLOR     = (24,  95,  165)
X_DARK      = (12,  68,  124)

O_FILL      = (250, 236, 231)
O_BORDER    = (240, 153, 123)
O_COLOR     = (153, 60,  29)
O_DARK      = (113, 43,  19)

WIN_FILL    = (234, 243, 222)
WIN_BORDER  = (151, 196, 89)
DRAW_FILL   = (241, 239, 232)

GREEN_DOT   = (99,  153, 34)
AMBER_DOT   = (239, 159, 39)
RED_DOT     = (226, 75,  74)

BADGE_D_BG  = (241, 239, 232)
BADGE_D_FG  = (110, 110, 120)

def mkfont(size, bold=False):
    return pygame.font.SysFont("Segoe UI, Arial", size, bold=bold)

F_TITLE = mkfont(28, True)
F_H2    = mkfont(20, True)
F_H3    = mkfont(16, True)
F_BODY  = mkfont(14)
F_SMALL = mkfont(12)
F_MARK  = mkfont(64, True)
F_PILL  = mkfont(13)

def rrect(surf, color, rect, r=10, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def blit_text(surf, txt, fnt, color, cx, cy, anchor="center"):
    s = fnt.render(str(txt), True, color)
    r = s.get_rect()
    if   anchor == "center": r.center   = (cx, cy)
    elif anchor == "left":   r.midleft  = (cx, cy)
    elif anchor == "right":  r.midright = (cx, cy)
    surf.blit(s, r)

def lerp_col(a, b, t):
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_winner(board):
    for a,b,c in WINS:
        if board[a] and board[a]==board[b]==board[c]:
            return board[a], (a,b,c)
    return None, None

def is_draw(board):
    return all(board) and check_winner(board)[0] is None

def available(board):
    return [i for i,v in enumerate(board) if not v]

def minimax(board, is_max, depth, alpha, beta):
    w, _ = check_winner(board)
    if w == "O": return 10 - depth
    if w == "X": return depth - 10
    if not available(board): return 0
    if is_max:
        best = -999
        for i in available(board):
            board[i] = "O"
            best = max(best, minimax(board, False, depth+1, alpha, beta))
            board[i] = None
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    else:
        best = 999
        for i in available(board):
            board[i] = "X"
            best = min(best, minimax(board, True, depth+1, alpha, beta))
            board[i] = None
            beta = min(beta, best)
            if beta <= alpha: break
        return best

def best_move(board, diff):
    moves = available(board)
    if not moves: return None
    if diff == "easy": return random.choice(moves)
    if diff == "medium" and random.random() < 0.5: return random.choice(moves)
    best_s, best_m = -999, None
    for i in moves:
        board[i] = "O"
        s = minimax(board, False, 0, -999, 999)
        board[i] = None
        if s > best_s: best_s, best_m = s, i
    return best_m

class Button:
    def __init__(self, rect, label, fnt, bg, fg, bc, r=8):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.fnt = fnt
        self.bg = bg; self.fg = fg; self.bc = bc; self.r = r
        self.hovered = False

    def draw(self, surf):
        bg = lerp_col(self.bg, self.bc, 0.12) if self.hovered else self.bg
        rrect(surf, bg, self.rect, self.r, 1, self.bc)
        s = self.fnt.render(self.label, True, self.fg)
        surf.blit(s, s.get_rect(center=self.rect.center))

    def update(self, mx, my): self.hovered = self.rect.collidepoint(mx, my)

    def clicked(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and e.button==1 and self.rect.collidepoint(e.pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock  = pygame.time.Clock()
        self.mode   = "2p"
        self.diff   = "hard"
        self.scores = {"X":0,"O":0,"D":0}
        self.history= []
        self.round  = 1
        self._build_buttons()
        self.new_game()

    def _build_buttons(self):
        self.b2p    = Button((W//2-120, 62, 110, 32), "2 Players", F_PILL, SURFACE, TEXT_PRI, BORDER, 16)
        self.bai    = Button((W//2+10,  62, 110, 32), "vs AI",     F_PILL, SURFACE, TEXT_SEC, BORDER, 16)
        self.beasy  = Button((W//2-170,102, 100, 28), "Easy",   F_SMALL, SURFACE, TEXT_SEC, BORDER, 14)
        self.bmed   = Button((W//2-60, 102, 110, 28), "Medium", F_SMALL, SURFACE, TEXT_SEC, BORDER, 14)
        self.bhard  = Button((W//2+60, 102, 100, 28), "Hard",   F_SMALL, SURFACE, TEXT_SEC, BORDER, 14)
        self.bnew   = Button((W//2-100,H-118, 90,34), "New game",  F_BODY, X_FILL, X_DARK,  X_BORDER)
        self.breset = Button((W//2+10, H-118, 90,34), "Reset all", F_BODY, SURFACE,TEXT_PRI, BORDER)
        self._style_pills()

    def _style_pills(self):
        for b,on in [(self.b2p,self.mode=="2p"),(self.bai,self.mode=="ai")]:
            b.bg = X_FILL if on else SURFACE
            b.fg = X_DARK if on else TEXT_SEC
            b.bc = X_BORDER if on else BORDER
        for b,d in [(self.beasy,"easy"),(self.bmed,"medium"),(self.bhard,"hard")]:
            on = (d == self.diff)
            b.bg = SURFACE if on else BG
            b.fg = TEXT_PRI if on else TEXT_HINT
            b.bc = (80,80,90) if on else BORDER

    def new_game(self):
        self.board      = [None]*9
        self.cur        = "X"
        self.over       = False
        self.win_cells  = ()
        self.winner     = None
        self.canim      = [0.0]*9
        self.win_anim   = 0.0
        self.ai_pending = False
        self.ai_timer   = 0
        self._mk_status()

    def _mk_status(self):
        if self.winner:
            self.stxt = f"{self._pname(self.winner)} wins this round!"
            self.sdot = "done"
        elif self.over:
            self.stxt = "Draw — no winner!"
            self.sdot = "done"
        elif self.ai_pending:
            self.stxt = "AI is thinking..."
            self.sdot = "think"
        else:
            self.stxt = f"{self._pname(self.cur)}'s turn — click a cell"
            self.sdot = "go"

    def _pname(self, mark):
        if self.mode=="ai" and mark=="O":
            return f"AI ({'Easy' if self.diff=='easy' else 'Medium' if self.diff=='medium' else 'Hard'})"
        return f"Player {'1' if mark=='X' else '2'}"

    def cell_rect(self, i):
        row,col = divmod(i,3)
        return pygame.Rect(BOARD_LEFT+col*CELL+5, BOARD_TOP+row*CELL+5, CELL-10, CELL-10)

    def play(self, i):
        if self.board[i] or self.over: return
        self.board[i] = self.cur
        self.canim[i] = 0.01
        w, cells = check_winner(self.board)
        if w:
            self.over=True; self.winner=w; self.win_cells=cells
            self.scores[w]+=1
            self.history.insert(0,{"round":self.round,"result":w,"opp":"AI" if self.mode=="ai" else "P2"})
            self.round+=1; self._mk_status()
            pygame.time.set_timer(pygame.USEREVENT+1, 2100, 1)
        elif is_draw(self.board):
            self.over=True
            self.scores["D"]+=1
            self.history.insert(0,{"round":self.round,"result":"D","opp":"AI" if self.mode=="ai" else "P2"})
            self.round+=1; self._mk_status()
            pygame.time.set_timer(pygame.USEREVENT+1, 1800, 1)
        else:
            self.cur = "O" if self.cur=="X" else "X"
            if self.mode=="ai" and self.cur=="O":
                self.ai_pending=True
                self.ai_timer=pygame.time.get_ticks()
            self._mk_status()

    def update(self, dt):
        for i in range(9):
            if 0 < self.canim[i] < 1:
                self.canim[i] = min(1.0, self.canim[i]+dt*7)
        if self.winner:
            self.win_anim = min(1.0, self.win_anim+dt*4)
        if self.ai_pending and not self.over:
            delay = {"easy":400,"medium":600,"hard":900}[self.diff]
            if pygame.time.get_ticks()-self.ai_timer > delay:
                self.ai_pending=False
                m = best_move(self.board, self.diff)
                if m is not None: self.play(m)

    def draw(self):
        s = self.screen
        s.fill(BG)

        blit_text(s,"Tic Tac Toe",F_TITLE,TEXT_PRI,W//2,32)

        self.b2p.draw(s); self.bai.draw(s)
        if self.mode=="ai":
            self.beasy.draw(s); self.bmed.draw(s); self.bhard.draw(s)

        sy = 140
        for cx,cw,lbl,val,bg,bc,lc,vc in [
            (W//2-220,80,"X wins", self.scores["X"],  X_FILL, X_BORDER, X_COLOR, X_DARK),
            (W//2-40, 80,"Draws",  self.scores["D"],  DRAW_FILL,BORDER,TEXT_SEC,TEXT_PRI),
            (W//2+80, 80,"O wins", self.scores["O"],  O_FILL, O_BORDER, O_COLOR, O_DARK),
        ]:
            rrect(s,bg,(cx,sy,cw,58),10,1,bc)
            blit_text(s,lbl,F_SMALL,lc,cx+cw//2,sy+17)
            blit_text(s,val,F_H2,vc,cx+cw//2,sy+39)

        py = 210
        for mark,px,fill,bord,mc in [
            ("X",BOARD_LEFT,X_FILL,X_BORDER,X_DARK),
            ("O",BOARD_LEFT+BOARD_SIZE//2+8,O_FILL,O_BORDER,O_DARK),
        ]:
            active = (self.cur==mark and not self.over)
            bg  = fill if active else SURFACE
            bc2 = bord if active else BORDER
            rrect(s,bg,(px,py,BOARD_SIZE//2-8,46),10,1,bc2)
            pygame.draw.circle(s,fill if not active else SURFACE,(px+23,py+23),14)
            pygame.draw.circle(s,bord,(px+23,py+23),14,1)
            blit_text(s,mark,F_H3,mc,px+23,py+23)
            blit_text(s,self._pname(mark),F_BODY,TEXT_PRI if active else TEXT_SEC,px+44,py+14,"left")
            blit_text(s,f"plays {mark}",F_SMALL,TEXT_HINT,px+44,py+32,"left")
            if active:
                pygame.draw.circle(s,GREEN_DOT,(px+BOARD_SIZE//2-18,py+23),5)

        rrect(s,SURFACE,(BOARD_LEFT-6,BOARD_TOP-6,BOARD_SIZE+12,BOARD_SIZE+12),14,1,BORDER)
        for i in 1,2:
            pygame.draw.line(s,BORDER,(BOARD_LEFT+i*CELL,BOARD_TOP+8),(BOARD_LEFT+i*CELL,BOARD_TOP+BOARD_SIZE-8),1)
            pygame.draw.line(s,BORDER,(BOARD_LEFT+8,BOARD_TOP+i*CELL),(BOARD_LEFT+BOARD_SIZE-8,BOARD_TOP+i*CELL),1)

        mx,my = pygame.mouse.get_pos()
        for i in range(9):
            v = self.board[i]
            cr= self.cell_rect(i)
            iw= i in self.win_cells

            if iw:
                t   = self.win_anim
                base= WIN_FILL if self.winner=="X" else O_FILL
                fill= lerp_col(SURFACE,base,t)
                bc2 = lerp_col(BORDER, WIN_BORDER if self.winner=="X" else O_BORDER, t)
            elif v=="X": fill=X_FILL;  bc2=X_BORDER
            elif v=="O": fill=O_FILL;  bc2=O_BORDER
            elif not self.over and not self.ai_pending and cr.collidepoint(mx,my):
                fill = X_FILL if self.cur=="X" else O_FILL
                bc2  = X_BORDER if self.cur=="X" else O_BORDER
            else:
                fill=BG; bc2=BORDER

            rrect(s,fill,cr,10,1,bc2)

            if v:
                t2    = self.canim[i]
                scale = (0.4+0.6*min(1,t2)) if t2<1 else 1.0
                col   = X_COLOR if v=="X" else O_COLOR
                sym   = "X" if v=="X" else "O"
                ms    = F_MARK.render(sym,True,col)
                sw,sh = int(ms.get_width()*scale), int(ms.get_height()*scale)
                if sw>0 and sh>0:
                    ms2 = pygame.transform.scale(ms,(sw,sh))
                    s.blit(ms2,(cr.centerx-sw//2,cr.centery-sh//2))

        if self.winner and self.win_cells and self.win_anim>0.2:
            a,_,c2  = self.win_cells
            r1,r2   = self.cell_rect(a), self.cell_rect(c2)
            lc      = X_COLOR if self.winner=="X" else O_COLOR
            alpha   = int(200*min(1,(self.win_anim-0.2)/0.8))
            ls      = pygame.Surface((W,H),pygame.SRCALPHA)
            pygame.draw.line(ls,(*lc,alpha),r1.center,r2.center,5)
            s.blit(ls,(0,0))

        stx,sty = BOARD_LEFT, BOARD_TOP+BOARD_SIZE+20
        t_osc   = (pygame.time.get_ticks()%800)/800
        dcol    = {"go":GREEN_DOT,"think":lerp_col(AMBER_DOT,(255,200,80),abs(math.sin(t_osc*math.pi))),"done":RED_DOT}[self.sdot]
        pygame.draw.circle(s,dcol,(stx+8,sty+1),5)
        blit_text(s,self.stxt,F_BODY,TEXT_SEC,stx+20,sty,"left")

        self.bnew.draw(s); self.breset.draw(s)

        hy = H-90
        rrect(s,SURFACE,(BOARD_LEFT,hy,BOARD_SIZE,78),12,1,BORDER)
        hcount=f"{len(self.history)} game{'s' if len(self.history)!=1 else ''}"
        blit_text(s,"Match history",F_SMALL,TEXT_SEC,BOARD_LEFT+12,hy+12,"left")
        blit_text(s,hcount,F_SMALL,TEXT_HINT,BOARD_LEFT+BOARD_SIZE-12,hy+12,"right")
        pygame.draw.line(s,BORDER,(BOARD_LEFT,hy+24),(BOARD_LEFT+BOARD_SIZE,hy+24),1)
        if not self.history:
            blit_text(s,"No games yet",F_SMALL,TEXT_HINT,W//2,hy+51)
        else:
            for idx,h in enumerate(self.history[:3]):
                hx  = BOARD_LEFT+12+idx*(BOARD_SIZE//3)
                hw  = BOARD_SIZE//3-14
                ry  = h["result"]
                if   ry=="X": bbg,bfg,bl = X_FILL,X_DARK,"X wins"
                elif ry=="O": bbg,bfg,bl = O_FILL,O_DARK,"O wins"
                else:         bbg,bfg,bl = BADGE_D_BG,BADGE_D_FG,"Draw"
                rrect(s,bbg,(hx,hy+32,hw,18),9)
                blit_text(s,bl,F_SMALL,bfg,hx+hw//2,hy+41)
                blit_text(s,f"R{h['round']} vs {h['opp']}",F_SMALL,TEXT_HINT,hx+hw//2,hy+62)

        pygame.display.flip()

    def handle(self, events):
        mx,my = pygame.mouse.get_pos()
        for b in [self.b2p,self.bai,self.beasy,self.bmed,self.bhard,self.bnew,self.breset]:
            b.update(mx,my)
        for e in events:
            if e.type==pygame.QUIT: return False
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: return False
            if e.type==pygame.USEREVENT+1: self.new_game()
            if self.b2p.clicked(e):    self.mode="2p"; self._style_pills(); self.new_game()
            if self.bai.clicked(e):    self.mode="ai"; self._style_pills(); self.new_game()
            if self.beasy.clicked(e):  self.diff="easy";   self._style_pills(); self.new_game()
            if self.bmed.clicked(e):   self.diff="medium"; self._style_pills(); self.new_game()
            if self.bhard.clicked(e):  self.diff="hard";   self._style_pills(); self.new_game()
            if self.bnew.clicked(e):   self.new_game()
            if self.breset.clicked(e):
                self.scores={"X":0,"O":0,"D":0}; self.history=[]; self.round=1; self.new_game()
            if (e.type==pygame.MOUSEBUTTONDOWN and e.button==1
                    and not self.over and not self.ai_pending
                    and not (self.mode=="ai" and self.cur=="O")):
                for i in range(9):
                    if self.cell_rect(i).collidepoint(e.pos) and not self.board[i]:
                        self.play(i); break
        return True

    def run(self):
        last = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()
            dt  = (now-last)/1000.0
            last= now
            if not self.handle(pygame.event.get()): break
            self.update(dt)
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
