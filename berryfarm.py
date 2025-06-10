from minescript import (
    getblock, player,
    player_set_orientation, player_press_use,
    player_press_sneak, player_look_at, echo
)
import threading
import time

def use_item_pulse():
    player_press_use(True)
    player_press_use(False)

def sneak_pulse():
    player_press_sneak(True)
    player_press_sneak(False)

RADIUS = 4
bushes = []

def find_bushes():
    echo("🧭 Scanning for bushes...")
    pos = player().position
    px, py, pz = [round(coord) for coord in pos]

    total_checks = (2 * RADIUS + 1) ** 3
    checked = 0

    for dx in range(-RADIUS, RADIUS + 1):
        for dy in range(-RADIUS, RADIUS + 1):
            for dz in range(-RADIUS, RADIUS + 1):
                bx = px + dx
                by = py + dy
                bz = pz + dz

                block = getblock(bx, by, bz)
                if block and block.startswith("minecraft:sweet_berry_bush") and any(f"age={n}" in block for n in [1, 2, 3]):
                    bushes.append((bx, by, bz))

                checked += 1
                if checked % 25 == 0:
                    percent = (checked / total_checks) * 100
                    echo(f"🔍 Scanning... {percent:.1f}%")

    echo(f"✅ Found {len(bushes)} bushes.")
    start_harvesting()

def start_harvesting():
    echo("🌾 Harvest Beginning")
    while True:
        for bx, by, bz in bushes:
            player_look_at(bx + 0.5, by + 0.5, bz + 0.5)
            threading.Thread(target=use_item_pulse).start()
            threading.Thread(target=sneak_pulse).start()
            time.sleep(0.1)

find_bushes()
