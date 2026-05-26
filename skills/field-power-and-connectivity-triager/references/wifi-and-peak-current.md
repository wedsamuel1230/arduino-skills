# WiFi And Peak Current

Use this reference when WiFi or radio behavior changes across power paths.

## Failure Pattern

Common report:

- board connects over USB
- board fails to connect or reboots on intended supply

That pattern often points to transient current demand or supply integrity, not
to SSID or password bugs.

## What To Check

- quality of the USB cable or alternate wiring path
- source current capability
- regulator transient behavior
- boot-time voltage sag during WiFi association

## Useful Questions

- does failure happen before IP assignment?
- does serial output suggest brownout or reboot?
- does the board remain alive but disconnected, or does it restart?
- is the problem worse with peripherals active?

## Practical Guidance

- reduce variables: test the same sketch on both paths
- avoid assuming a bench supply setting means the board actually sees that
  voltage under load
- remember that ESP32-class boards can have sharper current peaks than simpler
  MCU boards
