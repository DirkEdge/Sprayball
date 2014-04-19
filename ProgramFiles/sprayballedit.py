from livewires import games, color
import random
games.init(screen_width = 640, screen_height=480,fps = 50)

class Launcher(games.Sprite):
    """A MISSLE LAUNCHER TO POP BALLONS"""
    image = games.load_image("launcher.bmp", transparent = True)
    
    def __init__(self, y = 450):
        """initialize launcher"""
        super(Launcher, self).__init__(image = Launcher.image, x = games.mouse.x, y = y)
        #Establish Score on the screen (You may need to move this later)
        self.score = games.Text(value = 0, size = 25, color = color.black, x = 575, y = 20)
        games.screen.add(self.score)

    def update(self):
        """Move to Mouse Coordinates"""
        global LEVEL
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
            
##        if games.mouse.is_pressed(0):
##            print "left mouse button pressed"
##            self.score.value += 2
##            if self.score.value%100 == 0:
##                LEVEL += 1
##                if LEVEL == 6:
##                    LEVEL = 0
##                load_image(LEVEL)
            
        global MISSILE_WAIT
        MISSILE_WAIT -= 1
        if games.mouse.is_pressed(0) and MISSILE_WAIT < 0:
            #print "left mouse button pressed"
            new_missile = missile(self.left + 6, self.top)
            games.screen.add(new_missile)
            MISSILE_WAIT = 0 #25

        if games.mouse.is_pressed(2):
            print "Right Mouse Pressed"
            games.screen.quit()

def load_balloons():
    BALLOON_COUNT = 0
    Balloons = 1
    for y in range (50, 250, 20):
        for x in range (15, 635, 16):
            BALLOON_COUNT += 1
            color = random.choice([Balloons.RED, Balloons.BLUE, Balloons.GREEN, Balloons.YELLOW])
            new_balloon = Balloons(x = x, y = y, color = color)
            games.screen.add(new_balloon)
        return BALLOON_COUNT

def load_image(x):
    """Load the background image"""
    wall_image = games.load_image(FILES[x], transparent = False)
    games.screen.background = wall_image

def main():
    global MISSILE_WAIT
    global BALLOON_COUNT
    global FILES
    global LEVEL
    
    FILES=["file1.jpg","file2.jpg","file3.jpg","file4.jpg","file5.jpg","file6.jpg"]
    LEVEL = 0
    load_image(LEVEL)
    the_launcher = Launcher()
    games.screen.add(the_launcher)

    class Balloons(games.Sprite):
        RED = 1
        BLUE = 2
        GREEN = 3
        YELLOW = 4

        images = {RED : games.load_image("rBalloon.bmp"),
                  BLUE : games.load_image("bBalloon.bmp"),
                  GREEN : games.load_image("gBalloon.bmp"),
                  YELLOW : games.load_image("yBalloon.bmp")}

        def __init__(self,x,y,color):
            super(Balloons, self).__init__(
                image = Balloons.images[color],
                x = x, y = y)
            self.color = color

        def handle_collide(self):
            self.destroy()
            global BALLOON_COUNT
            global LEVEL
            BALLOON_COUNT -= 1
            if BALLOON_COUNT == 0:
                LEVEL += 1
                if LEVEL == 6:
                    LEVEL = 0
                load_image(LEVEL)
                BALLOON_COUNT = load_balloons()

    BALLOON_COUNT = load_balloons()
    
    games.mouse.is_visible = False
    #We will deal with this command later
    #games.screen.event_grab = True
    games.screen.mainloop()

    class missile(games.Sprite):
        global MISSILE_WAIT
        MISSILE_WAIT = 0
        image = games.load_image("missile.bmp")

        def __init__(self, x, y):

            super(missile, self).__init__(image = missile.image,
                                          x = x, y = y, dy = -7)

            def update(self):
                if self.top <= 50:
                    self.destroy()
                    self.check_collide()
                    
            def check_collide(self):
                for balloon in self.overlapping_sprites:
                    self.destroy()
                    balloon.handle_collide()

            def handle_collide(self):
                self.top = (self.top - self.height-10)



main()
