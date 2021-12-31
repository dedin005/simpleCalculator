import PySimpleGUI as sg
from inspect import signature
from collections import defaultdict

class Calculator():
    def __init__(self):
        self.layout = [

                       [sg.Text(size=(25,1), justification='right', key='output')],
                       [sg.Button('AC'),sg.Button('+/-'),sg.Button('%'),sg.Button('/')],
                       [sg.Button('7'),sg.Button('8'),sg.Button('9'),sg.Button('X')],
                       [sg.Button('4'),sg.Button('5'),sg.Button('6'),sg.Button('-')],
                       [sg.Button('1'),sg.Button('2'),sg.Button('3'),sg.Button('+')],
                       [sg.Button('0'),sg.Button('.'),sg.Button('='),sg.Button('Quit')]

                      ]
        self.window = sg.Window("Calculator", self.layout)
        self.prev = None
        self.d = False
        self.later = None
        self.save = 0
        self.c = False
        self.wasUpdated = False

        self.buttons = defaultdict(None)
        self.buttons['AC'] = self.clear 
        self.buttons['+/-']= self.negate 
        self.buttons['%']  = self.percent
        self.buttons['/']  = self.divide
        self.buttons['X']  = self.multiply
        self.buttons['-']  = self.subtract
        self.buttons['+']  = self.add
        self.buttons['=']  = self.result
        self.buttons['.']  = self.decimal
        self.buttons['0']  = self.update
        self.buttons['1']  = self.update
        self.buttons['2']  = self.update
        self.buttons['3']  = self.update
        self.buttons['4']  = self.update
        self.buttons['5']  = self.update
        self.buttons['6']  = self.update
        self.buttons['7']  = self.update
        self.buttons['8']  = self.update
        self.buttons['9']  = self.update

        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

            self.func = self.buttons[event]

            params = len(signature(self.func).parameters)
            if params == 1:
                if self.c:
                    self.c = False
                    self.window['output'].update('')
                ret = self.func(event)
                if ret != None:
                    self.window['output'].update('')
                    self.update(ret)

            elif params == 2:
                self.run()

            else:
                self.func()

            self.prev = self.func

            # if event == sg.WINDOW_CLOSED or event == 'Quit':
            #     break
            # if event == 'AC':
            #     print(self.window['output'])
            #     self.clear()
            # elif event == '':
            #     pass
            # elif num:
            #     self.update(event)

        self.window.close()

    ####################
    # Instance Methods #
    ####################

    # bookkeeping

    # doesn't work
    def result(self):
        self.c = True
        if self.later != None and self.wasUpdated:
            v = self.later(float(self.save), float(self.window['output'].get()))
            self.clear()
            if v == float(int(v)):
                v = int(v)
            self.update(v)
            self.later = None

    # 
    def clear(self):
        self.d = False
        self.window['output'].update("0")

    # 
    def update(self, a):
        s = self.window['output'].get()
        if s == '0':
            s = ''
        self.window['output'].update(s + str(a))
        return None

    # numerical

    def decimal(self):
        if self.d:
            return
        self.d = True
        if self.c:
            self.c = False
            self.window['output'].update('0.')
            return
        self.update('.')

    def percent(self):
        a = self.window['output'].get()
        self.window['output'].update('')
        self.update(float(a)/100)

    def negate(self):
        a = self.window['output'].get()
        self.window['output'].update('')
        self.update(-float(a))

    # calculations

    def run(self):
        self.wasUpdated = True
        if self.later != None:
            self.func(float(self.save), float(self.window['output'].get()))
        self.later = self.func
        self.save = float(self.window['output'].get())
        self.window['output'].update('')

    def multiply(self, a, b):
        return a*b

    def subtract(self, a, b):
        return self.add(a, -b)

    def add(self, a, b):
        return a+b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return self.multiply(a, 1/b)

c = Calculator()


