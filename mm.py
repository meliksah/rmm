# Copyright 2023 meliksah
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyautogui
import rumps
import random
import time
from scipy import interpolate
import numpy as np
import math

def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class RmmApp(rumps.App):
    def __init__(self):
        super(RmmApp, self).__init__("RMM", icon="icon.png")
        self.active = False
        self.timer = None
        self.active_button = rumps.MenuItem(title='Active', callback=self.toggle_active, key='a')

    def toggle_active(self, sender):
        self.active = not self.active
        self.active_button.state = self.active

        if self.active:
            self.timer = rumps.Timer(self.move_mouse, 5)
            self.timer.start()
        else:
            if self.timer:
                self.timer.stop()
                self.timer = None

    def move_mouse(self, sender):
        pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
        # Minimal number of seconds to sleep between mouse moves.
        pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
        # The number of seconds to pause after EVERY public function call.
        pyautogui.PAUSE = 0  # Default: 0.1
        cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
        x1, y1 = pyautogui.position()  # Starting position
        screen_width, screen_height = pyautogui.size() # Get screen size
        # Set bounds for random movement to within a single screen
        x2 = random.randint(0, screen_width)
        y2 = random.randint(0, screen_height)
        # Distribute control points between start and destination evenly.
        x = np.linspace(x1, x2, num=cp, dtype='int')
        y = np.linspace(y1, y2, num=cp, dtype='int')

        # Randomise inner points a bit (+-RND at most).
        RND = 10
        xr = [random.randint(-RND, RND) for k in range(cp)]
        yr = [random.randint(-RND, RND) for k in range(cp)]
        xr[0] = yr[0] = xr[-1] = yr[-1] = 0
        x += xr
        y += yr

        # Approximate using Bezier spline.
        degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
                                        # Must be less than number of control points.
        tck, u = interpolate.splprep([x, y], k=degree)
        # Move upto a certain number of points
        u = np.linspace(0, 1, num=2+int(point_dist(x1,y1,x2,y2)/50.0))
        points = interpolate.splev(u, tck)

        # Move mouse.
        duration = 0.1
        timeout = duration / len(points[0])
        point_list=zip(*(i.astype(int) for i in points))
        for point in point_list:
            pyautogui.moveTo(*point)
            time.sleep(timeout)

if __name__ == '__main__':
    app = RmmApp()
    app.menu = [app.active_button]
    app.run()
