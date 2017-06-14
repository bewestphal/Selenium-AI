class ActionSpace(object):

    def __init__(self, driver=None):
        self.driver = driver

        self.available_actions = [
            self.mouse_press,
            self.mouse_scroll_up,
            self.mouse_scroll_down,
            self.move_mouse_right,
            self.move_mouse_left,
            self.move_mouse_up,
            self.move_mouse_down
        ]

        self.number_of_actions = len(self.available_actions)

        self.mouse_position_x = 0
        self.mouse_position_y = 0

    def mouse_press(self):
        return [[
            (('PointerEvent', self.mouse_position_x, self.mouse_position_y, 1)),
            (('PointerEvent', self.mouse_position_x, self.mouse_position_y, 0))
        ]]

    def mouse_scroll_up(self):
        scroll_height = self.driver.execute_script("return document.documentElement.scrollTop")
        self.driver.execute_script("window.scrollBy(0, {scroll_position});"
                                   .format(scroll_position=scroll_height - 50))
        return self.set_mount_position()

    def mouse_scroll_down(self):
        scroll_height = self.driver.execute_script("return document.documentElement.scrollTop")
        self.driver.execute_script("window.scrollBy(0, {scroll_position});"
                                   .format(scroll_position=scroll_height + 50))
        return self.set_mount_position()

    def move_mouse_right(self):
        self.mouse_position_x += 15
        return self.set_mount_position()

    def move_mouse_left(self):
        self.mouse_position_x -= 15
        return self.set_mount_position()

    def move_mouse_down(self):
        self.mouse_position_y += 15
        return self.set_mount_position()

    def move_mouse_up(self):
        self.mouse_position_y -= 15
        return self.set_mount_position()

    def reset_mouse_position(self):
        window_size = self.driver.get_window_size()
        window_position = self.driver.get_window_position()

        self.mouse_position_x = (window_size["width"] + window_position["x"]) / 2
        self.mouse_position_y = (window_size["height"] + window_position["y"]) / 2 + 25

        return self.set_mount_position()

    def set_mount_position(self):
        return [[('PointerEvent', self.mouse_position_x, self.mouse_position_y, False)]]