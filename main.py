import pyautogui
import time
import win32api
import win32con
import keyboard

drag_delay = 0.02

garbage_check = (1270, 530)
garbage_up = (1265, 415)
garbage_down = (1265, 800)
garbage_col0r = (145, 175, 187)

card_swipe_check = (900, 800)
card_swipe_color = (222, 223, 222)
card_swipe_hidden = (825, 800)
card_swipe_left = (715, 460)
card_swipe_right = (1500, 460)

left_positions = [(570, 275), (570, 460), (570, 645), (570, 835)]
right_positions = [(1315, 275), (1315, 460), (1315, 645), (1315, 835)]


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def drag_mouse(start, end, hold=0, duration=0.0):
    win32api.SetCursorPos(start)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(drag_delay)
    pyautogui.moveTo(end[0], end[1], duration)
    time.sleep(hold)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(drag_delay)


def report(pic):
    rgb = pic.getpixel((1808, 683))
    if rgb == (221, 34, 0):
        print("reporting body")
        click(1800, 700)


def wires(pic):
    left_colors = []
    right_colors = []

    actions = []

    for v in left_positions:
        left_colors.append(pic.getpixel(v))

    for v in right_positions:
        right_colors.append(pic.getpixel(v))

    for k in range(len(left_colors)):
        for key in range(len(right_colors)):
            if left_colors[k] == right_colors[key]:
                actions.append([left_positions[k], right_positions[key]])

    if len(actions) > 3:
        for k in actions:
            drag_mouse(k[0], k[1], 0)
        return True
    return False


def garbage(pic):
    if pic.getpixel(garbage_check) == garbage_col0r:
        click(card_swipe_hidden[0], card_swipe_hidden[1])
        time.sleep(0.2)
        drag_mouse(garbage_up, garbage_down, 3)
        return True
    return False


def swipe_card(pic):
    if pic.getpixel(card_swipe_check) == card_swipe_color:
        click(825, 800)
        time.sleep(0.5)
        drag_mouse(card_swipe_left, card_swipe_right, 0, 1.15)
        return True
    return False


if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('q'):
            p = pyautogui.screenshot()
            if swipe_card(p):
                continue
            if garbage(p):
                continue
            if wires(p):
                continue
            report(p)
        time.sleep(0.1)
