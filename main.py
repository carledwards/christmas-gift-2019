
import gifviewer
from ht16k33_matrix import Matrix8x8x2
import time
import random
import machine
import ssd1306
from machine import Pin
from machine import Timer

_oled = None
_led_display = None


_blank = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_up_arrow = (
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 3, 3, 3, 3, 0, 0],
    [0, 3, 0, 3, 3, 0, 3, 0],
    [3, 0, 0, 3, 3, 0, 0, 3],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
)

_happy_face = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_sad_face = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 0, 0],
    [0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_numb_face = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_red_light = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_yellow_light = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

_green_light = (
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
)

def show_image(image, y_offset=0, forced_color=None):
    global _led_display
    for row_index in range(0, len(image)):
        row = image[row_index]
        for col_index in range(0, len(row)):
            color = row[col_index]
            if forced_color and color:
                color = forced_color
            _led_display.pixel(col_index, row_index+y_offset, color)
    _led_display.show()

def dim_to_bright(delay=.1):
    global _led_display
    for brightness in range(0,16):
        _led_display.brightness(brightness)
        if delay:
            time.sleep(delay)

def bright_to_dim(delay=.1):
    global _led_display
    for brightness in range(15,-1,-1):
        _led_display.brightness(brightness)
        if delay:
            time.sleep(delay)

def startup():
    global _led_display
    _led_display.brightness(0)
    show_image(_sad_face)
    for _ in range(0, 2):
        dim_to_bright()
    _led_display.brightness(0)
    show_image(_numb_face)
    for _ in range(0, 2):
        dim_to_bright()
    _led_display.brightness(0)
    show_image(_happy_face)
    dim_to_bright()


def scanner(menu_id):
    global _led_display
    stop_point = None
    while _current_menu == menu_id:
        for index in range(0,8):
            if not stop_point:
                stop_point = random.randint(12, 88)
            _led_display.fill(0)
            _led_display.brightness(0)
            _led_display.pixel(index, 4, 2)
            _led_display.show()
            dim_to_bright(.008)
            stop_point -= 1
            if stop_point <= 0:
                stop_point = None
                time.sleep(.5 * random.randint(1, 7))

def knight_rider(menu_id):
    while _current_menu == menu_id:
        for index in range(0,7):
            _led_display.fill(0)
            _led_display.brightness(0)
            _led_display.pixel(index, 4, 2)
            _led_display.show()
            dim_to_bright(.005)
        for index in range(7,0,-1):
            _led_display.fill(0)
            _led_display.brightness(0)
            _led_display.pixel(index, 4, 2)
            _led_display.show()
            dim_to_bright(.005)

def race_game(menu_id):
    global _led_display
    show_image(_blank)
    player_value = None
    while _current_menu == menu_id:
        if not player_value:
            _led_display.brightness(0)
            player_value = [0,0,0]
            show_image(_red_light)
            dim_to_bright(.02)
            time.sleep(.3)
            if _current_menu != menu_id:
                break
            bright_to_dim(.03)
            show_image(_yellow_light)
            dim_to_bright(.02)
            time.sleep(.3)
            if _current_menu != menu_id:
                break
            bright_to_dim(.02)
            show_image(_green_light)
            dim_to_bright(.02)
            time.sleep(.3)
            if _current_menu != menu_id:
                break
            bright_to_dim(.02)
            _led_display.fill(0)
            _led_display.show()
            _led_display.brightness(15)

        buffer = (
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        )
        # select which player is going to get the move
        player = random.randint(1,3)
        move = random.randint(0,2)
        if move == 2:
            move = -1
        player_value[player-1] += move

        for player_index in range(0,3):
            if player_value[player_index] < 0:
                player_value[player_index] = 0
            elif player_value[player_index] >= 8:
                player_value[player_index] = 8
                # if a player gets up to the top, they only get a 1-in-3 chance of winning
                if not random.randint(1,100) % 3 == 0:
                    player_value[player_index] = 7

            for i in range(0, player_value[player_index]):
                color = 2
                if i >=  5:
                    color = 3
                if player_value[player_index] == 8:
                    color = 1
                buffer[7-i][player_index*2+player_index] = color
                buffer[7-i][player_index*2+player_index+1] = color

        show_image(buffer)
        if 8 in player_value:
            time.sleep(5)
            player_value = None
        else:
            time.sleep(.12)


def eq(menu_id):
    global _led_display
    show_image(_blank)
    col_size = [0, 0, 0, 0, 0, 0, 0, 0]
    while _current_menu == menu_id:
        screen_buffer = (
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        )
        for col_index in range(0, len(col_size)):
            step = random.randint(0,2)
            if step == 2:
                step = -1
            col_size[col_index] += step
            if col_size[col_index] < 0:
                col_size[col_index] = 0
            elif col_size[col_index] > 8:
                col_size[col_index] = 8
            for i in range(0, col_size[col_index]):
                if i == col_size[col_index]-1:
                    screen_buffer[7-i][col_index] = 3
                else:
                    screen_buffer[7-i][col_index] = 1
        show_image(screen_buffer)
        time.sleep(.1)

def starfield(menu_id):
    global _led_display
    quadrant_def = [[3,3,-1,-1], [4,3,1,-1], [4,4,1,1], [3,4,-1,1]]
    star_locations = []
    while _current_menu == menu_id:
        # Generate a new star
        # 
        # select 1 of 4 quadrants
        #
        #    0  |  1
        #  -----+-----
        #    3  |  2
        #
        no_of_stars = random.randint(1,2)
        for _ in range(0,no_of_stars):
            quadrant = random.randint(0,3)
            color = random.randint(1,3)

            slot_index = None
            for i in range(0, len(star_locations)):
                if star_locations[i][0] == None:
                    slot_index = i
                    break
            slot_entry = [quadrant, 0, 0, color]
            if slot_index is not None:
                star_locations[slot_index] = slot_entry
            else:
                star_locations.append(slot_entry)

        # display the stars
        _led_display.fill(0)
        for star in star_locations:
            quad_id = star[0]
            x = star[1]
            y = star[2]
            col = star[3]

            # skip ones that have moved off the screen
            if star[0] == None or x in (-4,4) or y in (-4,4):
                star[0] = None  # make the slot unused
                continue

            # display the pixel
            _led_display.pixel(
                x + quadrant_def[quad_id][0],
                y + quadrant_def[quad_id][1],
                col)
            _led_display.show()

            # pick next step
            direction = random.randint(1,3)
            if direction == 1 or direction == 3:
                x += quadrant_def[quad_id][2]
            if direction == 2 or direction == 3:
                y += quadrant_def[quad_id][3]
            star[1] = x
            star[2] = y

        time.sleep(.1)

def turn_off(menu_id):
    while _current_menu == menu_id:
        time.sleep(.1)

def binary_scroll(menu_id):
    counter = 0x00
    color = 1
    while _current_menu == menu_id:
        col = 0
        _led_display.scroll(0,-1)
        for b in range(7, -1, -1):
            if counter & 2**b == 2**b:
                _led_display.pixel(7-b, 7, color)
            else:
                _led_display.pixel(7-b, 7, 0)
        counter += 1
        counter = counter & 0xFF
        if counter == 0:
            color += 1
            if color > 3:
                color = 1
        _led_display.show()
        time.sleep(.1)

def init_displays():
    global _oled, _led_display
    oled_rst = Pin(16, Pin.OUT)
    oled_rst.value(1)
    i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
    _oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    _led_display = Matrix8x8x2(i2c)
    _led_display.fill(0)
    _led_display.show()

_current_menu = 0
_reset_timer_flag = True
_timer_count = 0
_next_button_time = 0
_in_startup = True
_oled_has_been_reset = False

def timer_cb(timer_id):
    global _reset_timer_flag
    global _timer_count
    global _oled_has_been_reset
    global _next_button_time
    if _reset_timer_flag:
        _timer_count = 0
        _next_button_time = 0
        _reset_timer_flag = False
        _oled_has_been_reset = False
    else:
        _timer_count += 1

    # hide the mode name after 5 seconds
    if _oled_has_been_reset == False and _timer_count > 50 and _current_menu >= 3:
        _oled_has_been_reset = True
        _oled.fill(0)
        _oled.show()

def button_cb(p):
    global _next_button_time, _current_menu, _reset_timer_flag
    if _timer_count > _next_button_time :
        print("button cb, current menu:", _current_menu)
        _next_button_time = _timer_count + 4
        if _current_menu != 0:
            _reset_timer_flag = True
            _current_menu += 1
            gifviewer.stop()

if __name__ == '__main__':
    _current_menu = 0

    init_displays()

    timer = Timer(1)
    timer.init(mode=Timer.PERIODIC, period=100, callback=timer_cb)

    select_button = Pin(2 , Pin.IN, Pin.PULL_UP)
    select_button.irq(trigger=Pin.IRQ_FALLING, handler=button_cb)
    while True:
        _led_display.fill(0)
        _oled.fill(0)
        if _current_menu == 0:
            _oled.text('Christmas', 0, 0, 1)
            _oled.text('2019', 0, 10, 1)
            _oled.show()
            startup()
            _current_menu = 1
            _in_startup = True
            continue
        elif _current_menu == 1:
            show_image(_happy_face)
            if not gifviewer.run(_oled, 'fuzzy', one_shot=True):
                time.sleep(4)
            if _in_startup:
                _current_menu = 2
            continue
        elif _current_menu == 2:
            if _in_startup:
                _oled.text('select mode', 0, 0, 1)
                _oled.text('with button', 0, 10, 1)
                show_image(_up_arrow, y_offset = 7-(_timer_count % 8))
            else:
                _current_menu = 3
                continue
        elif _current_menu == 3:
            _in_startup = False
            _oled.text('Gaze', 0, 0, 1)
            _oled.show()
            starfield(3)
        elif _current_menu == 4:
            _oled.text('Worm race', 0, 0, 1)
            _oled.show()
            race_game(4)
        elif _current_menu == 5:
            _oled.text('Equalizer', 0, 0, 1)
            _oled.show()
            eq(5)
        elif _current_menu == 6:
            _oled.text('COPs', 0, 0, 1)
            _oled.show()
            scanner(6)
        elif _current_menu == 7:
            _oled.text('81n42y', 0, 0, 1)
            _oled.show()
            binary_scroll(7)
        elif _current_menu == 8:
            _oled.text('Knight Rider', 0, 0, 1)
            _oled.show()
            knight_rider(8)
        elif _current_menu == 9:
            _oled.text('Sleep shhh', 0, 0, 1)
            _oled.show()
            _led_display.show()
            turn_off(9)
        else:
            _current_menu = 1

        _oled.show()
        _led_display.show()
        time.sleep(.1)
