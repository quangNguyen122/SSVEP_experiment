#!/usr/bin/env python
"""Display 4
"""

from VisionEgg import *
start_default_logging(); watch_exceptions()

from VisionEgg.Core import *
from VisionEgg.FlowControl import Presentation, FunctionController
from VisionEgg.MoreStimuli import *
from VisionEgg.Text import Text
from VisionEgg.Textures import *
import time

class Stimulation:
    global TopRate, BotRate, LeftRate, RightRate, HSize, VSize
    global numTrial, order_appear
    global duration_cue, duration_target, duration_trial, total_time
    # Set up stimulus's frequency
    TopRate =   5              # Hz
    BotRate = 10
    LeftRate = 15
    RightRate = 20

    # Set dimension of the targets
    HSize = 100
    VSize = 50

    # Experiment parameters
    numTrial = 10
    order_appear = np.uint16(4*np.random.random(numTrial)+1)
    duration_target = 3
    duration_cue = 2
    duration_trial = duration_target + duration_cue
    total_time = duration_trial*numTrial

    def __init__(self):
        global w, h
        self._running = True

        # Initialize screen
        self.screen = get_default_screen()

        # Get dimension of the screen
        w = self.screen.size[0]
        h = self.screen.size[1]

        # Initialize Targets
        self.TopTarget = Target2D()
        self.BotTarget = Target2D()
        self.LeftTarget = Target2D()
        self.RightTarget = Target2D()

        # Message
        self.text = Text(text='Please wait for next trial...',
                         color=(1.0, 0.5, 0.5),
                         position=(w/2, h*0.8),
                         font_size=50,
                         anchor='center',
                         on=False)

        # Arrows
        self.arrow = TextureStimulus()

        # Viewports to stick graphical objects to screen
        self.viewport1 = Viewport(screen=self.screen,
                                  stimuli=[self.TopTarget, self.BotTarget, self.LeftTarget, self.RightTarget])      # For Targets
        self.viewport2 = Viewport(screen=self.screen,
                                  stimuli=[self.text, self.arrow])                                                  # For cue (and other things)

        # Presentations (for controlling timing)
        self.p = Presentation(go_duration=(duration_target, 'seconds'), viewports=[self.viewport1])
        self.p2 = Presentation(go_duration=(duration_cue, 'seconds'), viewports=[self.viewport2])

    def on_init(self):
        # Set screen's background color
        self.screen.set(bgcolor=(0., 0., 0.)) # black

        # Set target's properties
        self.TopTarget.set(size=(HSize, VSize),
                           color= (1.0, 1.0, 1.0, 1.0),
                           position=(w/2, h*0.8))
        self.BotTarget.set(size=(HSize, VSize),
                           color=(1.0, 1.0, 1.0, 1.0),
                           position=(w/2, h*0.2))
        self.LeftTarget.set(size=(VSize, HSize),
                            color=(1.0, 1.0, 1.0, 1.0),
                            position=(w*0.2, h/2))
        self.RightTarget.set(size=(VSize, HSize),
                             color=(1.0, 1.0, 1.0, 1.0),
                             position=(w*0.8, h/2))

        # Message
        # self.text.set(text='Please wait for next trial...',
        #               color=(1.0, 0.5, 0.5),
        #               position=(w/2, h*0.8),
        #               font_size=50,
        #               anchor='center',
        #               on=False)

        # Arrows
        self.arrow.set(texture=Texture('images\left2.bmp'),
                        position=(w/2, h/2),
                        anchor='center',
                        on=False)

        # Set control's parameters and corresponding function. Controlling targers
        self.p.add_controller(self.TopTarget, 'on',     FunctionController(during_go_func=self.topFlick))
        self.p.add_controller(self.BotTarget, 'on',     FunctionController(during_go_func=self.botFlick))
        self.p.add_controller(self.LeftTarget, 'on',    FunctionController(during_go_func=self.leftFlick))
        self.p.add_controller(self.RightTarget, 'on',   FunctionController(during_go_func=self.rightFlick))

        # Controlling others
        # self.p2.add_controller(self.text, 'on',         FunctionController(during_go_func=self.appear))
        self.p2.add_controller(self.arrow, 'on',        FunctionController(during_go_func=self.arrow_appear))
        self.p2.add_controller(self.arrow, 'texture',   FunctionController(during_go_func=self.random_cue))

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        for i in range(0,numTrial):
            self.p.go()
            self.p2.go()

    #################################################
    # Controlling methods: Flickering               #
    #################################################
    def topFlick(self,t):
        return int(t*TopRate*2.0) % 2

    def botFlick(self,t):
        return int(t*BotRate*2.0) % 2

    def leftFlick(self,t):
        return int(t*LeftRate*2.0) % 2

    def rightFlick(self,t):
        return int(t*RightRate*2.0) % 2

    def arrow_appear(self, t):
        flag = True
        if flag:
            #self.writedata(t, 1)
            flag = False

        if self.p.is_in_go_loop():
            return False
        else:
            return True

    def random_cue(self,t):
        start_time = self.p.last_go_loop_start_time_absolute_sec
        # if not isinstance(start_time, type(None)):
        try:    # catch the wrong type of start_time returned earlier
            i = int(start_time/duration_trial)
        finally:
            return Texture('images/left2.bmp')  # Just return something

        cur_target = order_appear[i]        # current target
        if cur_target == 1:
            return Texture('images/left2.bmp')
        elif cur_target == 2:
            return Texture('images/right2.bmp')
        elif cur_target == 3:
            return Texture('images/up2.bmp')
        elif cur_target == 4:
            return Texture('images/down2.bmp')

    #################################################
    # Writing data methods                          #
    #################################################
    def on_writing(self):
        # Open file for writing data
        self.file = open("Recordingfile.txt", "w")

    def on_close(self):
        self.file.close()

    def writedata(self, time, target_flag):
        line = str(time) + '\t' + str(target_flag) + '\n'
        file.write(line)

"""
    Main
"""
if __name__ == "__main__":
    exp = Stimulation()
    exp.on_execute()