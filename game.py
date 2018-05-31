import pygame
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Force static position of screen

##problems
#jumping through pages seems to be an issue
#alpha.transfer was before the update and so failed

#Colors:
WHITE = (255, 255, 255)
GREEN = (89, 75, 57)
BLUE = (0, 0, 205)
YELLOW = (210, 210, 0)
ORANGE = (205, 19, 0)
SKY = (0, 0, 100)
BLACK = (0, 0, 0)
BROWN = (109, 95, 77)
LIGHT_GREY = (155, 155, 155)
RED = (109, 5, 5)
AQUA = (0, 0, 75)

#parameters:
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1500

SHIP_WIDTH = SHIP_HEIGHT = 50
PIXEL_WIDTH = PIXEL_HEIGHT = 50
COUNT = 0


class Game:
    def __init__(self):
        #intial objects
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1500, 1000), pygame.SRCALPHA)
        self.screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.caption = pygame.display.set_caption('GAME BOY')
        self.container = pygame.Rect(100, 150, PIXEL_WIDTH, PIXEL_HEIGHT)

        #stage of game:
        self.on = True
        self.play = False
        self.op = True
        self.end = False
        self.start = False

        #counters:
        self.fps = 60
        self.time = 0

        #gravity
        self.attract = 5
        self.pull = True

        # for page transfers
        self.scott = 0
        self.old = 0

        self.transfer = True
        self.six_change = False
        self.page = ""

        # key variables
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.interact = False

    def boot(self):
        if self.interact:
            self.start = True

    def gravity(self, alpha, platform_group,block_group):
        if self.pull:
            alpha.rect.y += 10
            jacob = pygame.sprite.spritecollide(alpha, platform_group, False)
            if len(jacob) > 0:
                for p in jacob:
                    alpha.rect.bottom = p.rect.top
                    alpha.onGround = True
            #else:
            #    alpha.onGround = False

        for b in block_group:
            b.rect.y += 10
            b.remove(platform_group)

            if len(pygame.sprite.spritecollide(b, platform_group, False)) > 0:
                platform_group.add(b)
                b.rect.y -= 10
            else:
                platform_group.add(b)

    def interact_check(self, alpha, ladder_group):
        self.pull = True

        if alpha.jumping or alpha.moving or alpha.swimming:
            self.pull = False

        for a in ladder_group:
            if a.check:
                self.pull = False

    def key_check(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                if e.key == pygame.K_UP:
                    self.up = True
                if e.key == pygame.K_DOWN:
                    self.down = True
                if e.key == pygame.K_LEFT:
                    self.left = True
                if e.key == pygame.K_RIGHT:
                    self.right = True
                if e.key == pygame.K_SPACE:
                    self.interact = True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.up = False
                if e.key == pygame.K_DOWN:
                    self.down = False
                if e.key == pygame.K_RIGHT:
                    self.right = False
                if e.key == pygame.K_LEFT:
                    self.left = False
                if e.key == pygame.K_SPACE:
                    self.interact = False

    def bg(self):
        pass

    def page_check(self):
        if self.scott == 0:
            self.page = [
                " RRR                           ",
                " RRR                           ",
                " RRR                           ",
                " RRR                           ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                         V     ",
                "           Y                    ",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]
        elif self.scott == 1:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "           S        PPPPPPPPPPP",
                "                               ",
                "                               ",
                "  G                            ",
                "          S                    ",
                "                    G          ",
                "                               ",
                "                               ",
                "                               ",
                "        S               G      ",
                "                PPP            ",
                " G                             ",
                "                               ",
                "             D                 ",
                "                               ",
                "              S                ",
                "                        PPPPPPP"]

        elif self.scott == 2:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "PPPPPPPHPPPPPPPPPPPPPPPPPPPPPPP",
                "       H  PccccccccccP         ",
                "       H  PccccccccccP         ",
                "       H  PccccYcccccP         ",
                "       H  PcccPPPccccP         ",
                "       H  PcccPPPccccc          ",
                "  PPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
                "  PccccccccccccccccccccPccccP  ",
                "  PccccccccccccccccccccPccccP  ",
                "  PcccccccccPccPcccccccPccccP  ",
                "  cccccccPccPccPcccccccPccccP  ",
                " HccccPccccccccPccccccaccGccP  ",
                " HPPPPPPPPPPPPPPPPPPPPPPccccP  ",
                " HPcccccccccPcccccccPcccccccP  ",
                " HPccccccPccPcccPcccccccccccP  ",
                " HPccccccPccccccPcccPcccccccc ",
                "PPPccccPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 3:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "PPPPPPPPPPPP                   ",
                "                      D        ",
                "                           G   ",
                "                               ",
                "                               ",
                "PPP          D                 ",
                "                    S          ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "        PPPPPP                 ",
                "     PPPPP                     ",
                "PPPPPPPP                       "]

        elif self.scott == 4:
            self.page = [
                "                            PP",
                "                             c",
                "                             c",
                "                             P",
                "                      PPHPPPP ",
                "                        H     ",
                "                        H     ",
                "                   PPHPPPP    ",
                "                     H        ",
                "                     H        ",
                "                     H    PPPP",
                "                    PPPPPP    ",
                "                              ",
                "                              ",
                "                              ",
                "                              ",
                "                              ",
                "              PPPPPPP         ",
                "PPPPWWWWWWWWWWWWWWWWPPPP       ",
                "PPPPPPPPPWWWWWWWWWWWPPPPPPPPPPP"]

        elif self.scott == 5:
            self.page = [
                "PPPccccPPPPPPPPPPPPPPPPPPPPP  ",
                "ccccccccccPccccccccccccccccP   ",
                "ccccccPPPcaccccccccccccccccP   ",
                "PPPPPPPPPPPPcccccccccccccccP  ",
                "   PcccccccccccccccccccccccP  ",
                "   PccccccccccccPPcccccccccP  ",
                "   PccccPPPPPccccccPPccccccP  ",
                "   ccccccccccccccccccccccccP  ",
                "   ccccccccccccccccccccPPPPP  ",
                "   PPPPPcccccccccccccccccccP  ",
                "PPPPcccccccccccccccPPPcccccP  ",
                "   PccccccccccccccccccccccPP  ",
                "   PcccccPPPPPPPPPPPPPPPPPPP  ",
                "   PcccccccccccccccccccccccP  ",
                "   PPPPccccccccccccccccccccP  ",
                "   PcccccccccccccccccccccccP  ",
                "   PccccPPcccccccccccccccccP  ",
                "   ccccccccccccccccccccccccP  ",
                "   cccccacccccccccccccccccca  ",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 6 and not self.six_change:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "      RRRRRRRRRR               ",
                "     RRRRRRRRRRRR              ",
                "      BBBBBBBBBB               ",
                "      BBV BBBBBB               ",
                "      BB  BBBBBB               ",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 6 and self.six_change:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "      RRRRRRRRRR               ",
                "     RRRRRRRRRRRR              ",
                "      BBBBBBBBBB               ",
                "      BB      BB               ",
                "      BB     FBB               ",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 7:
            self.page = [
                "PPPPPPPPPPWWWWWWWWWWPPPPPPPPPP",
                "PPPPPPPPPPPPPWWWWWWWPPPPPPPPPP",
                "WWWWWWWWWWWWWWWWWWWWWWWWPPPPPP",
                "WWWWWWWWWWaPWWWaWWWWWWWWPPPPPPP",
                "WWWWWPPPPPPPPPPPPPPWWPPPPWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWP",
                "WWWWWWWWWPPPPPPPPPPPPPPPPPPPPP",
                "WWWWWWWWWPPPPPP        PPPPPPP",
                "WWWWWWWWWPPPPPP  PPPP  PPPPPPP",
                "WWWWWWWWWWWWWWWWWPPPPWWWWWWWWP",
                "WWWWWWWWWWWWWWWWWPPPPPPPPPWWWW",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPWWW",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 8:
            self.page = [
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
                "PPPPPPPPPPPPPPPPPP         PPP",
                "PPPPPPPPPPPPPPPPPP         PPP",
                "P                          PPP",
                "PP                    X    PPP",
                "PP                         PPP",
                "PP    PPPPPPPPP     PPPPPPPPPP",
                "P  G      PPPPPPPPPPPPPPPPPPPP",
                "PP        PPPPPPPP  PPPPPPPPPP",
                "PP       PP  PPPPPPPPPPPPPPPPP",
                "P                            P",
                "PP    PP                     P",
                "PP    P P                    P",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPHHPP",
                "PPPPPPPPPPPPPPP      PPPPPHHPP",
                "PP      PPPPPPPPPPPPPPPPP HH P",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWHHWP",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWHHWP",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

        elif self.scott == 9:
            self.page = [
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "                               ",
                "               P               ",
                "              PPP              ",
                "             PPPPP             ",
                "            PPPPPPP            ",
                "           PPPPPPPPP           ",
                "          PPPPPPPPPPP          ",
                "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

    def dump(self, platform_group, interact_group, pass_group, ladder_group, move_group, water_group, text_group,
             flash_group, block_group):
        platform_group.empty()
        interact_group.empty()
        pass_group.empty()
        ladder_group.empty()
        move_group.empty()
        water_group.empty()
        text_group.empty()
        flash_group.empty()
        block_group.empty()

    def level_builder(self, platform_group, interact_group, pass_group, ladder_group, move_group, water_group,
                      text_group, flash_group, block_group):
        global COUNT
        if self.scott != self.old:
            self.old = self.scott
            self.dump(platform_group, interact_group, pass_group, ladder_group, move_group, water_group, text_group,
                      flash_group, block_group)
            self.page_check()
            self.transfer = True
        if self.transfer:
            x = y = 0
            self.page_check()
            for row in self.page:
                for col in row:
                    if col == "P":
                        p = Platform(x, y, self)
                        platform_group.add(p)
                    elif col == "a":
                        a = Block(x, y, self, platform_group)
                        block_group.add(a)
                        interact_group.add(a)
                        platform_group.add(a)
                        if self.scott == 5 or self.scott == 2:
                            p = Back(x, y, self, LIGHT_GREY)
                            pass_group.add(p)
                        if self.scott == 7:
                            p = Water(x, y)
                            water_group.add(p)

                    elif col == "B":
                        a = Back(x, y, self, GREEN)
                        pass_group.add(a)
                    elif col == "R":
                        a = Back(x, y, self, RED)
                        pass_group.add(a)
                    elif col == 'z':
                        a = Back(x, y, self, BLACK)
                        pass_group.add(a)
                    elif col == 'c':
                        a = Back(x, y, self, LIGHT_GREY)
                        pass_group.add(a)
                    elif col == "V":
                        v = Door(x, y, self, YELLOW)
                        interact_group.add(v)
                    elif col == "H":
                        h = Ladder(x, y, self)
                        ladder_group.add(h)
                    elif col == "G":
                        COUNT += 1
                        g = Slidders(x, y, self, COUNT)
                        move_group.add(g)
                        if self.scott == 2:
                            p = Back(x - 50, y, self, LIGHT_GREY)
                            a = Back(x, y, self, LIGHT_GREY)
                            pass_group.add(p, a)
                    elif col == "S":
                        COUNT += 1
                        s = Drifters(x, y, self, 50, COUNT)
                        move_group.add(s)
                    elif col == "D":
                        COUNT += 1
                        s = Drifters(x, y, self, 0, COUNT)
                        move_group.add(s)
                    elif col == "Y":
                        meh = Key(x, y, self)
                        interact_group.add(meh)
                        if self.scott == 2:
                            p = Back(x, y, self, LIGHT_GREY)
                            pass_group.add(p)
                    elif col == "F":
                        f = Flash(x, y)
                        interact_group.add(f)
                    elif col == "W":
                        w = Water(x, y)
                        water_group.add(w)
                    elif col == "X":
                        c = Chest(x, y, self)
                        interact_group.add(c)
                    x += 50
                y += 50
                x = 0
        self.transfer = False


class Hero(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        #base parameters:
        self.image = pygame.image.load("images/squirtle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(150, 200, SHIP_WIDTH, SHIP_HEIGHT)

        self.container = container

        #moving constants:
        self.xspeed = 10
        self.yspeed = 12
        self.force = 0

        #moving conditions:
        self.onGround = True
        self.moving = False
        self.jumping = False
        self.can_jump = True
        self.climbing = False
        self.falling = False
        self.swimming = False
        self.base_platform = 0

        #items:
        self.key = 0
        self.chest = 1

        #collision variables
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def update(self, platform_group, game, move_group):
        self.page_transfer(game)
        if game.up and self.can_jump:
            self.jumping = True
            self.onGround = False

        if not self.onGround:
            self.can_jump = False
        else:
            self.can_jump = True

        self.jump(platform_group, move_group, game)

        if game.left:
            self.image = pygame.image.load("images/squirtle-2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIXEL_WIDTH, PIXEL_HEIGHT))
            self.rect.x -= self.xspeed
            if len(pygame.sprite.spritecollide(self, platform_group, False)) > 0:
                self.rect.x += self.xspeed

        if game.right:
            self.image = pygame.image.load("images/squirtle.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIXEL_WIDTH, PIXEL_HEIGHT))
            self.rect.x += self.xspeed
            if len(pygame.sprite.spritecollide(self, platform_group, False)) > 0:
                self.rect.x -= self.xspeed

        self.collision_check(platform_group, move_group, game)

        if not game.start:
            self.rect.clamp_ip(self.container)

    def jump(self, block_group, move_group, game):

        if self.jumping:
            self.rect.y -= self.force
            self.force = self.yspeed - 0.5

            self.yspeed = self.force

            if self.yspeed < -12.5:
                self.onGround = True
                self.rect.y += self.yspeed + 1
                self.jump_reset()

            self.collision_check(block_group, move_group, game)

    def jump_reset(self):
        self.jumping = False
        self.yspeed = 12
        self.force = 0

    def collision_check(self, platform_group, move_group, game):
        hit_plats = pygame.sprite.spritecollide(self, platform_group, False)
        hit_slid = pygame.sprite.spritecollide(self, move_group, False)
        #platforms
        if len(hit_plats) > 0:
            for p in hit_plats:
                if self.force < 0 or game.pull:
                    if self.rect.bottom >= p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.jump_reset()
                        self.onGround = True
                if self.force > 0:
                    if self.rect.top <= p.rect.bottom:
                        self.rect.top = p.rect.bottom
                        self.jump_reset()

        if len(hit_slid) > 0:
            for p in hit_slid:
                if self.force < 0 or game.pull:
                    if self.rect.bottom >= p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.jump_reset()
                        self.onGround = True
                        self.base_platform = p.identity
                #if self.force > 0:
                #    if self.rect.top <= p.rect.bottom:
                #        self.rect.top = p.rect.bottom
                #        self.jump_reset()

        else:
            self.moving = False
            self.onGround = False

    def page_transfer(self, game):
        #123
        #456
        #789
        if game.scott == 0:
            if self.rect.x < 0:
              self.rect.x = 0
              print("NO ENTRY")

            if self.rect. x > SCREEN_WIDTH - PIXEL_WIDTH:
              self.rect.x  = SCREEN_WIDTH - PIXEL_WIDTH
              print("NO ENTRY")

            if self.rect.y < 0:
                self.rect.y = 0
                print("NO ENTRY")

            if self.rect.y > SCREEN_HEIGHT - PIXEL_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - PIXEL_HEIGHT
                print("NO ENTRY")

        elif game.scott == 1:
            if self.rect.x < 0:
                print("NO ENTRY")
                self.rect.x = 0

            if self.rect.x > SCREEN_WIDTH - 10:
                print('2')
                game.scott = 2
                self.rect.x = 10

            elif self.rect.y < 0:
                print("NO ENTRY")
                self.rect.y = 0

            elif self.rect.y > SCREEN_HEIGHT - 10:
                print('4')
                game.scott = 4
                self.rect.y = 10

        elif game.scott == 2:
            if self.rect.x < 0:
                print('1')
                self.rect.x = SCREEN_WIDTH - 10
                game.scott = 1

            elif self.rect.x > SCREEN_WIDTH - 10:
                print('3')
                self.rect.x = 10
                game.scott = 3
            elif self.rect.y < 0:
                print("NO ENTRY")
                self.rect.y = 0

            elif self.rect.y > SCREEN_HEIGHT:
                print("5")
                game.scott = 5
                self.rect.y = 10

        elif game.scott == 3:
            if self.rect.x < 0:
                print('2')
                game.scott = 2
                self.rect.x = SCREEN_WIDTH - 10

            elif self.rect.x > SCREEN_WIDTH - PIXEL_WIDTH:
                print("NO ENTRY")
                self.rect.x = SCREEN_WIDTH - PIXEL_WIDTH

            elif self.rect.y < 0:
                print("NO ENTRY")
                self.rect.y = 0

            elif self.rect.y > SCREEN_WIDTH - 10:
                print('6')
                game.scott = 6
                self.rect.y = 10

        elif game.scott == 4:
            if self.rect.x < 0:
                print("NO ENTRY")
                self.rect.x = 0

            if self.rect.x > SCREEN_WIDTH - 10:
                print('5')
                game.scott = 5
                self.rect.x = 10

            elif self.rect.y > SCREEN_WIDTH - 100:
                print('7')
                game.scott = 7
                self.rect.y = 10

            elif self.rect.y < 0:
                print('1')
                game.scott = 1
                self.rect.y = SCREEN_HEIGHT - 10

        elif game.scott == 5:
            if self.rect.x <= 0:
                print("4")
                game.scott = 4
                self.rect.x = SCREEN_WIDTH - 10

            elif self.rect.x > SCREEN_WIDTH - 10:
                print('6')
                game.scott = 6
                self.rect.x = 10

            elif self.rect.y > SCREEN_HEIGHT - 10:
                print('8')
                game.scott = 8
                self.rect.y = 10

            elif self.rect.y < 0:
                print('2')
                game.scott = 2
                self.rect.y = SCREEN_HEIGHT - 10

        elif game.scott == 6:
            if self.rect.x <= 0:
                print('5')
                game.scott = 5
                self.rect.x = SCREEN_WIDTH - 10

            if self.rect.x > SCREEN_WIDTH - PIXEL_WIDTH:
                print("NO ENTRY")
                self.rect.x = SCREEN_WIDTH - PIXEL_WIDTH

            elif self.rect.y < 0:
                print('3')
                game.scott = 3
                self.rect.y = SCREEN_HEIGHT - 10

            elif self.rect.y > SCREEN_WIDTH - 10:
                print('NO ENTRY')
                self.rect.y = 10


        elif game.scott == 7:
            if self.rect.x < 0:
                print("NO ENTRY")
                self.rect.x = 0

            if self.rect.x > SCREEN_WIDTH - 10:
                print('8')
                game.scott = 8
                self.rect.x = 10

            elif self.rect.y < 0:
                print(4)
                game.scott = 4
                self.rect.y = SCREEN_HEIGHT - 10

            elif self.rect.y > SCREEN_WIDTH - 10:
                print("NO ENTRY")
                self.rect.y -= PIXEL_HEIGHT

        elif game.scott == 8:
            if self.rect.x < 0:
                print('7')
                game.scott = 7
                self.rect.x = SCREEN_WIDTH - 10

            elif self.rect.x > SCREEN_WIDTH - 10:
                print('NO ENTRY')
                self.rect.x = SCREEN_WIDTH - PIXEL_WIDTH

            elif self.rect.y < 0:
                print("5")
                game.scott = 5
                self.rect.y = SCREEN_HEIGHT - 10

            elif self.rect.y > SCREEN_WIDTH:
                print("NO ENTRY")
                self.rect.y = SCREEN_WIDTH - PIXEL_HEIGHT

        elif game.scott == 9:
            if self.rect.x < 0:
                self.rect.x = 0
                print("NO ENTRY")

            if self.rect. x > SCREEN_WIDTH - PIXEL_WIDTH:
                self.rect.x  = SCREEN_WIDTH - PIXEL_WIDTH
                print("NO ENTRY")

            if self.rect.y < 0:
                self.rect.y = 0
                print("NO ENTRY")

            if self.rect.y > SCREEN_HEIGHT - PIXEL_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - PIXEL_HEIGHT
                print("NO ENTRY")


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.image.fill(BLACK)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, game, platform_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.image.fill(BLUE)
        self.move = 10
        self.platform_group = platform_group
        self.ground = False

    def interact(self, ship_group, game):
        for alpha in ship_group:
            if game.left and self.rect.top == alpha.rect.top:
                if self.rect.right == alpha.rect.left:
                    self.rect.x -= self.move
                    self.remove(self.platform_group)
                    if len(pygame.sprite.spritecollide(self, self.platform_group, False)) > 0:
                        self.platform_group.add(self)
                        self.rect.x += self.move
                    else:
                        self.platform_group.add(self)
            if game.right and self.rect.top == alpha.rect.top:
                if self.rect.left == alpha.rect.right:
                    self.rect.x += self.move
                    self.remove(self.platform_group)
                    if len(pygame.sprite.spritecollide(self, self.platform_group, False)) > 0:
                        self.platform_group.add(self)
                        self.rect.x -= self.move
                    else:
                        self.platform_group.add(self)


class Back(pygame.sprite.Sprite):
    def __init__(self, x, y, game, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.image.fill(color)


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.image.fill(RED)
        self.check = False

    def interact(self, ship_group, game):
        for alpha in ship_group:
            self.check = False
            if alpha.rect.bottom >= self.rect.top:
                if alpha.rect.y <= self.rect.y + 40:
                    if game.interact:

                        if self.rect.right >= alpha.rect.left >= self.rect.left:
                            if alpha.rect.bottom == self.rect.top:
                                alpha.rect.y += 5
                            self.check = True
                            alpha.rect.y -= 5

                        elif self.rect.left <= alpha.rect.right <= self.rect.right:
                            if alpha.rect.bottom == self.rect.top:
                                alpha.rect.y += 5
                            self.check = True
                            alpha.rect.y -= 5


class Slidders(pygame.sprite.Sprite):
    def __init__(self, x, y, game, count):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/cloud 2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (2 * PIXEL_WIDTH + 25, PIXEL_HEIGHT + 25))
        self.image_rect = pygame.Rect(x - 12.5, y - 12.5, 2 * PIXEL_WIDTH, PIXEL_HEIGHT + 25)
        self.rect = pygame.Rect(x, y, 2 * PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.timer = 30
        self.reset = 60
        self.identity = count

    def update(self, alpha):
        if self.timer > 0:
            self.timer -= 1
            self.rect.y += 5
            self.image_rect.y += 5
            if alpha.jumping or alpha.rect.top > self.rect.bottom or alpha.base_platform != self.identity:
                pass
            elif self.rect.top - 25 < alpha.rect.bottom <= self.rect.top:
                if alpha.rect.left + 50 >= self.rect.left and alpha.rect.right - 50 <= self.rect.right:
                    alpha.moving = True
                    alpha.onGround = True
                    alpha.rect.bottom = self.rect.top
                else:
                    alpha.onGround = False
                    alpha.moving = False
        if self.timer < 0:
            self.timer += 1
            self.rect.y -= 5
            self.image_rect.y -= 5
            if alpha.jumping or alpha.rect.top > self.rect.bottom or alpha.base_platform != self.identity:
                pass
            elif self.rect.top - 50 < alpha.rect.top <= self.rect.top:
                if alpha.rect.left + 50 >= self.rect.left and alpha.rect.right - 50 <= self.rect.right:
                    alpha.moving = True
                    alpha.onGround = True
                    alpha.rect.bottom = self.rect.top
                else:
                    alpha.onGround = False
                    alpha.moving = False
        if self.timer == 0:
            self.timer = -self.reset
            self.reset = self.timer


class Drifters(pygame.sprite.Sprite):
    def __init__(self, x, y, game, start, count):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/cloud 2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,( 3 * PIXEL_WIDTH + 100, PIXEL_HEIGHT + 100))
        self.image_rect = pygame.Rect(x - 50, y - 50 , 3 * PIXEL_WIDTH, PIXEL_HEIGHT)
        self.rect = pygame.Rect(x, y, 3 * PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.timer = start
        self.reset = 100
        self.identity = count

    def update(self, alpha):
        if self.timer > 0:
            self.timer -= 1
            self.rect.x += 5
            self.image_rect.x += 5
            if alpha.jumping or alpha.rect.top > self.rect.bottom or alpha.base_platform != self.identity:
                pass
            elif self.rect.top - 25 < alpha.rect.bottom <= self.rect.top:
                if alpha.rect.left + 50 >= self.rect.left and alpha.rect.right - 50 <= self.rect.right:
                    alpha.moving = True
                    alpha.onGround = True
                    alpha.rect.bottom = self.rect.top
                    alpha.rect.x += 5

                else:
                    alpha.onGround = True
                    alpha.moving = False

        elif self.timer < 0:
            self.timer += 1
            self.rect.x -= 5
            self.image_rect.x -= 5
            if alpha.jumping or alpha.rect.top > self.rect.bottom or alpha.base_platform != self.identity:
                pass
            elif self.rect.top - 25 < alpha.rect.bottom <= self.rect.top:
                if alpha.rect.left + 50 >= self.rect.left and alpha.rect.right - 50 <= self.rect.right:
                    alpha.moving = True
                    alpha.onGround = True
                    alpha.rect.bottom = self.rect.top
                    alpha.rect.x -= 5

                else:
                    alpha.onGround = True
                    alpha.moving = False

        if self.timer == 0:
            self.timer = -self.reset
            self.reset = self.timer


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.convert(game.screen)
        self.image.fill(YELLOW)

    def interact(self, ship_group, game):
        for alpha in ship_group:
            if game.interact:
                if self.rect.left < alpha.rect.left < self.rect.right or self.rect.left < alpha.rect.right < self.rect.right:
                    self.kill()
                    alpha.key = 1


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, game, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2 * PIXEL_WIDTH, 2 * PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, 2 * PIXEL_WIDTH, 2 * PIXEL_HEIGHT)
        self.image.fill(color)
        self.game = game

        #conditions
        self.open = False

    def lock(self, alpha):
        if self.open and self.game.scott == 0:
            self.game.scott = 6
            self.game.op = False
            self.game.play = True
            self.open = False
            alpha.key = 0

        if self.open and self.game.scott == 6:
            self.game.six_change = True
            self.game.old = 5

    def interact(self, ship_group, game):
        for alpha in ship_group:
            if game.interact and self.rect.bottom >= alpha.rect.bottom >= self.rect.bottom:
                if self.rect.left < alpha.rect.left < self.rect.right or self.rect.left > alpha.rect.right > self.rect.right:
                    if alpha.key == 1:
                        self.open = True
                    else:
                        print("Seems to be locked")
            self.lock(alpha)


class Flash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)

    def interact(self, ship_group, game):
        for alpha in ship_group:
            if game.interact:
                if self.rect.left < alpha.rect.left < self.rect.right or self.rect.left > alpha.rect.right > self.rect.right:
                    alpha.chest = True
                    self.kill()


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, PIXEL_WIDTH, PIXEL_HEIGHT)
        self.image.fill(AQUA)

    def swim(self, ship_group, game, platform_group):
        swimming = pygame.sprite.spritecollide(self, ship_group, False)
        for alpha in ship_group:
            alpha.swimming = False

        for obj in swimming:
            if game.interact:
                obj.swimming = True
                obj.rect.y -= 7.5
                crash = pygame.sprite.spritecollide(obj, platform_group, False)
                if len(crash) > 0:
                    for sprite in crash:
                        obj.rect.top = sprite.rect.bottom
            else:
                obj.swimming = False


class Text(pygame.sprite.Sprite):
    def __init__(self, font, x, y, a, flash):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = font.render(str(a), 1, BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.flash = flash

    def update(self, game):
        if self.flash:
            cur_time = pygame.time.get_ticks()

            if ((cur_time - game.time) % 1500) < 750:
                game.screen.blit(self.image, self.rect)


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (2 * PIXEL_WIDTH, 2 * PIXEL_HEIGHT))
        self.rect = pygame.Rect(x, y, 2 * PIXEL_WIDTH, 2 * PIXEL_HEIGHT)
        self.game = game

        #interact variables:
        self.open = False

    def update(self):
        if self.open and self.game.scott == 8:
            self.game.scott = 9
            self.game.play = False
            self.game.end = True

    def interact(self, ship_group, game):
        for alpha in ship_group:
            if game.interact and self.rect.bottom >= alpha.rect.bottom >= self.rect.bottom:
                if self.rect.left < alpha.rect.left < self.rect.right or self.rect.left > alpha.rect.right > self.rect.right:
                    if alpha.chest == 1:
                        self.open = True
                    else:
                        print("Seems to be locked")
            self.update()

def main():
    # initialize variable
    pygame.init()
    game = Game()
    font1 = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 50)
    title_font = pygame.font. Font(None, 200)

    #Text files:
    title_text = Text(title_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT/3, "GAME BOY", True)
    op_screen = Text(font2, SCREEN_WIDTH/2, SCREEN_HEIGHT * 1/2, "ARROW KEYS to move", False)
    op_screen_2 = Text(font2, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 2 + 50, "SPACE to interact", False)
    op_screen_3 = Text (font2, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1/2 + 100 , "UP to jump", False)
    end_screen = Text(font1, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "YOU WIN!", True)

    # Create Objects
    alpha = Hero(game.container)

    # Create Groups
    pass_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    interact_group = pygame.sprite.Group()
    ladder_group = pygame.sprite.Group()
    move_group = pygame.sprite.Group()
    ship_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    text_group = pygame.sprite.Group()
    flash_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    end_text = pygame.sprite.Group()

    #adding objects

    text_group.add(title_text, op_screen, op_screen_2, op_screen_3)
    flash_group.add(op_screen)
    end_text.add(end_screen)
    ship_group.add(alpha)

    #game
    while game.on:
        while game.op:

            #background checks:
            game.boot()
            game.key_check()
            game.screen.fill(WHITE)
            game.clock.tick(game.fps)
            game.interact_check(alpha, ladder_group)
            game.gravity(alpha, platform_group, block_group)

            #updates
            for b in interact_group:
                b.interact(ship_group, game)
            for H in ladder_group:
                H.interact(ship_group, game)
            for alpha in ship_group:
                alpha.update(platform_group, game, move_group)
            for text in text_group:
                text.update(game)

            #bliting onto screen:
            for text in text_group:
                if not text.flash:
                    game.screen.blit(text.image, text.rect)
            for I in interact_group:
                game.screen.blit(I.image, I.rect)
            for a in ship_group:
                game.screen.blit(a.image, a.rect)
            for p in platform_group:
                game.screen.blit(p.image, p.rect)
            for p in pass_group:
                game.screen.blit(p.image, p.rect)

            game.level_builder(platform_group, interact_group, pass_group, ladder_group, move_group, water_group,
                               text_group, flash_group, block_group)

            # Writes to main surface
            pygame.display.flip()

        while game.play:

            #background checks
            game.key_check()
            game.bg()
            game.screen.fill(SKY)
            game.clock.tick(game.fps)
            game.interact_check(alpha, ladder_group)
            game.gravity(alpha, platform_group, block_group)

            #updates:
            for b in interact_group:
                b.interact(ship_group, game)
            for H in ladder_group:
                H.interact(ship_group, game)
            for w in water_group:
                w.swim(ship_group, game, platform_group)
            for alpha in ship_group:
                alpha.update(platform_group, game, move_group)
                alpha.page_transfer(game)
            for m in move_group:
                m.update(alpha)

            #bliting onto screen:
            for c in pass_group:
                game.screen.blit(c.image, c.rect)
            for w in water_group:
                game.screen.blit(w.image, w.rect)
            for H in ladder_group:
                game.screen.blit(H.image, H.rect)
            for p in platform_group:
                game.screen.blit(p.image, p.rect)
            for b in interact_group:
                game.screen.blit(b.image, b.rect)
            for a in ship_group:
                game.screen.blit(a.image, a.rect)
            for m in move_group:
                game.screen.blit(m.image, m.image_rect)
                #game.screen.blit(m.image, m.rect)

            game.level_builder(platform_group, interact_group, pass_group, ladder_group, move_group, water_group,
                               text_group, flash_group, block_group)
            # Writes to main surface
            pygame.display.flip()

        while game.end:
            #background checks:
            game.key_check()
            game.screen.fill(WHITE)
            game.clock.tick(game.fps)
            game.interact_check(alpha, ladder_group)
            game.gravity(alpha, platform_group, block_group)

            #updates:
            for b in interact_group:
                b.interact(ship_group, game)
            for H in ladder_group:
                H.interact(ship_group, game)
            for w in water_group:
                w.swim(ship_group, game, platform_group)
            for alpha in ship_group:
                alpha.update(platform_group, game, move_group)
                alpha.page_transfer(game)
            for m in move_group:
                m.update(alpha)
            for text in end_text:
                text.update(game)

            #bliting onto screen:
            for text in end_text:
                if not text.flash:
                    game.screen.blit(text.image, text.rect)
            for H in ladder_group:
                game.screen.blit(H.image, H.rect)
            for c in pass_group:
                game.screen.blit(c.image, c.rect)
            for p in platform_group:
                game.screen.blit(p.image, p.rect)
            for b in interact_group:
                game.screen.blit(b.image, b.rect)
            for m in move_group:
                game.screen.blit(m.image, m.rect)
            for a in ship_group:
                game.screen.blit(a.image, a.rect)

            game.level_builder(platform_group, interact_group, pass_group, ladder_group, move_group, water_group,
                               text_group, flash_group, block_group)
            # Writes to main surface
            pygame.display.flip()


if __name__ == '__main__':
        main()
