import machine
import micropython

micropython.alloc_emergency_exception_buf(100)


class RCWL_0516:
    def __init__(self):
        self.pin = None
        self.interrupts = False
        self._on = self.pin.value()

    def begin(self, signalPin, useInterrupt=True):
        self.pin = machine.Pin(signalPin, machine.Pin.IN)
        self.interrupts = useInterrupt
        self._on = self.pin.value()
        if useInterrupt:
            self.pin.irq(
                trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
                handler=self._callback,
            )

    def end(self):
        self.interrupts = False
        self.pin.irq(trigger=None)
        self.pin = None

    def isOn(self):
        if self.interrupts == False:
            self._on = self.pin.value()
        return self._on

    def _callback(self, p):
        self._on = p.value()

    def test(self):
        last = self._on
        while True:
            if last != self._on:
                print(f"pin change {self._on}")
                last = self._on

