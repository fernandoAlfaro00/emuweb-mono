from evdev import UInput, AbsInfo, ecodes as e
import os
import asyncio
import websockets
import json

# Mapeo entre teclas y botones del gamepad virtual
KEY_MAPPING = {
    'a': e.BTN_A,
    's': e.BTN_B,
    'A': e.BTN_A,
    'S': e.BTN_B,
    'Enter': e.BTN_START,
    'Shift': e.BTN_SELECT,
    'ArrowLeft': e.BTN_DPAD_LEFT,
    'ArrowRight': e.BTN_DPAD_RIGHT,
    'ArrowUp': e.BTN_DPAD_UP,
    'ArrowDown': e.BTN_DPAD_DOWN
}

# Mapeo NES: A, B, Start, Select, y la cruceta (D-Pad)
capabilities = {
    e.EV_KEY: [
        e.BTN_A,        # NES A
        e.BTN_B,        # NES B
        e.BTN_START,    # NES Start
        e.BTN_SELECT,   # NES Select
        e.BTN_DPAD_UP,
        e.BTN_DPAD_DOWN,
        e.BTN_DPAD_LEFT,
        e.BTN_DPAD_RIGHT
    ]
}

# Crear el dispositivo virtual
ui = UInput(events=capabilities,
            name="VirtualGamepad0",
            bustype=e.BUS_USB)

ui1 = UInput(events=capabilities,
            name="VirtualGamepad1",
            bustype=e.BUS_USB)

# Variables para llevar el registro de teclas presionadas
pressed_keys_player0 = set()
pressed_keys_player1 = set()
async def handler(websocket):
    
    async for message in websocket:
        try:
            print("Cliente conectado en '/' (raíz)")
            data = json.loads(message)
            print(data)
            key = data.get("key")
            player = data.get("player")
            event = data.get("event")

            if key in pressed_keys_player0 and event == 'keydown' and player == '0':
                continue  # Evita repetir si ya está presionado

            if key in pressed_keys_player1 and event == 'keydown' and player == '1':
                continue  # Evita repetir si ya está presionado

            if event == "keydown" and player == '0':
                pressed_keys_player0.add(key)
                print("player 0 Presionado tecla "+key)
                if key in KEY_MAPPING:
                    code = KEY_MAPPING[key]
                    if code in [e.BTN_A, e.BTN_B, e.BTN_START, e.BTN_SELECT ,  e.BTN_DPAD_UP, e.BTN_DPAD_DOWN, e.BTN_DPAD_LEFT, e.BTN_DPAD_RIGHT ]:
                        ui.write(e.EV_KEY, code, 1)
                    ui.syn()

            elif event == "keyup" and player == '0':
                pressed_keys_player0.remove(key)
                print("player 0 Soltando tecla "+key)
                if key in KEY_MAPPING:
                    code = KEY_MAPPING[key]
                    if code in [e.BTN_A, e.BTN_B, e.BTN_START, e.BTN_SELECT ,  e.BTN_DPAD_UP, e.BTN_DPAD_DOWN, e.BTN_DPAD_LEFT, e.BTN_DPAD_RIGHT ]:
                        ui.write(e.EV_KEY, code, 0)
                    ui.syn()


            if event == "keydown" and player == '1':
                pressed_keys_player1.add(key)
                print("player 1 Presionado tecla "+key)
                if key in KEY_MAPPING:
                    code = KEY_MAPPING[key]
                    if code in [e.BTN_A, e.BTN_B, e.BTN_START, e.BTN_SELECT ,  e.BTN_DPAD_UP, e.BTN_DPAD_DOWN, e.BTN_DPAD_LEFT, e.BTN_DPAD_RIGHT ]:
                        ui1.write(e.EV_KEY, code, 1)
                    ui1.syn()

            elif event == "keyup" and player == '1':
                pressed_keys_player1.remove(key)
                print("player 1 Soltando tecla "+key)
                if key in KEY_MAPPING:
                    code = KEY_MAPPING[key]
                    if code in [e.BTN_A, e.BTN_B, e.BTN_START, e.BTN_SELECT ,  e.BTN_DPAD_UP, e.BTN_DPAD_DOWN, e.BTN_DPAD_LEFT, e.BTN_DPAD_RIGHT ]:
                        ui1.write(e.EV_KEY, code, 0)
                    ui1.syn()

        except Exception as ex:
            print("Error:", ex)


async def main():
    print(f'Iniciado server...')
    async with websockets.serve(handler,"",8090):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())