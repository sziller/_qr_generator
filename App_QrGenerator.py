import sys
import os
import pyqrcode
import tkinter


def app_qr_generator(mode: int, *args, **kwargs):
    """=== Function name: app_qr_generator_init ========================================================================
    :param mode: int -  1 - display as pixels in terminal window
                        2 - display in OS window
                        4 - write to file
    ============================================================================================== by Sziller ==="""

    print("Please enter sting to be converted into QR code below!")
    string = input("Your string: ")
    qrcode = pyqrcode.create(content=string)

    if mode in [1, 3, 5, 7]:
        print(qrcode.terminal())

    if mode in [2, 3, 6, 7]:
        qrcode_xbm = qrcode.xbm(scale=20)
        top = tkinter.Tk()
        qrcode_bmp = tkinter.BitmapImage(data=qrcode_xbm)
        qrcode_bmp.config(background="white")

        label = tkinter.Label(image=qrcode_bmp)
        label.pack()

        top.mainloop()

    # qrcode.svg('uca-url.svg', scale=10)

    if mode in [4, 5, 6, 7]:
        print("Please enter a fullfilename (with path) to save it, or hit enter to skip")
        answer = False
        while not answer:
            answer = input(str("Enter filename: <or skip - >: "))
            if answer == "-":
                break
            elif answer:
                qrcode.png(file=answer, scale= 36)


if __name__ == "__main__":
    try:
        # When starting from icon:
        arg01 = int(sys.argv[1])
    # ------------------------------------------------------
    except IndexError:
        # When starting from IDLE:
        arg01 = 7  # local init returns an image onscreen
    # ------------------------------------------------------

    app_qr_generator(mode=arg01)