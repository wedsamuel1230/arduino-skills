# Upload, Boot, Power, And Firmware Recovery

Use this reference before a recovery action. Stop driving external loads and
disconnect hazardous power when a fault could damage people, equipment, or the
board.

## Failed Upload

1. Confirm the exact board, board package/framework, FQBN or environment, port,
   cable, permissions, and tool version.
2. Run board/port discovery and a compile-only check; preserve the full error.
3. Try a known-good data cable, direct USB path, and the board's documented
   bootloader/reset sequence. Do not randomly change pins or erase storage.
4. Check whether another process owns the port and whether power is stable.
5. Only use erase, bootloader repair, or vendor recovery when the board-specific
   procedure and data-loss impact are known.

## Boot Failure Or Boot Loop

- Disconnect external loads and test the smallest known-good image.
- Check strapping/boot pins, reset cause, watchdog, brownout, flash layout,
  partition size, and serial boot logs.
- Reflash a known-good image through the documented recovery path, then restore
  application features one change at a time.
- Preserve the previous image and configuration when rollback is possible.

## Power Fault

- Measure voltage at the board and load during startup and peak activity.
- Check regulator headroom, USB limits, wiring, ground, polarity, connectors,
  inrush, thermal behavior, and shared-load transients.
- Do not infer current safety from nominal voltage alone; use measured or
  datasheet peak current and a margin.

## Corrupted Firmware Or Field Recovery

- Identify the device, image version, bootloader state, and last known-good
  image before writing anything.
- Prefer signed, versioned images with an atomic update and rollback slot.
- Use a physical or documented recovery path that does not depend on the failed
  network or application task.
- Record the recovery result and leave the device in a safe default state.
