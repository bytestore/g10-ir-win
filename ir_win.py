# -------------------------------
# Programming IR buttons on Windows
# For Google G10 reference remote, Homatics B21, etc
# 
# Install Python with PATH
# upgrade pip
# python -m pip install --upgrade pip
# install bleak
# python pip install bleak
# or
# python -m pip install bleak
#
# 1 Run script with remote BT mac
# python ir_win.py 75-A0-90-E8-E7-0F
# 2 on remote press BACK+HOME
# -------------------------------


import asyncio
import sys
from bleak import BleakClient, BleakScanner, BleakError

# UUID 
CHARACTERISTIC_UUID_PROGRAM_STARTSTOP = "d343bfc1-5a21-4f05-bc7d-af01f617b664"
CHARACTERISTIC_UUID_PROGRAM_KEY = "d343bfc2-5a21-4f05-bc7d-af01f617b664"
CHARACTERISTIC_UUID_PROGRAM_VALUE = "d343bfc3-5a21-4f05-bc7d-af01f617b664"
g
async def write(client, characteristic, value: bytes):
    """Write with pause ."""
    try:
        await client.write_gatt_char(characteristic, value)
        print(f"Write  {characteristic}: {value.hex()}")
        await asyncio.sleep(0.2)
    except Exception as e:
        print(f"Error write {characteristic}: {e}")


async def program_code(client, key, value_hex):
    """Send Key + Value."""
    await write(client, CHARACTERISTIC_UUID_PROGRAM_KEY, key)
    await write(client, CHARACTERISTIC_UUID_PROGRAM_VALUE, bytes.fromhex(value_hex))


async def program_start(client):
    await write(client, CHARACTERISTIC_UUID_PROGRAM_STARTSTOP, b"\x01")


async def program_stop(client):
    await write(client, CHARACTERISTIC_UUID_PROGRAM_STARTSTOP, b"\x00")

async def run(address):
    print(f"Connect to {address} ...")
    try:
        async with BleakClient(address, timeout=15.0) as client:
            if not client.is_connected:
                print("Couldnt connect.")
                return

            print("Connected!")

            # buttons and IR codes
            codes_to_program = [
                [b"\x00\x18", "0221017c0020123c000c001a000c0040000c001a000c001a000c001a000c0040000c001a000c001a000c001a000c0040000c0040000c0040000c0040000c001a000c001a000c05f4000c001a000c0040000c001a000c001a000c001a000c001a000c0040000c0040000c0040000c001a000c001a000c001a000c001a000c0040000c0040000c05f4"],  # VolUp
                [b"\x00\x19", "0221017c0020123c000c001a000c0040000c001a000c001a000c001a000c001a000c0040000c001a000c001a000c0040000c0040000c0040000c0040000c001a000c001a000c05f4000c001a000c0040000c001a000c001a000c001a000c0040000c001a000c0040000c0040000c001a000c001a000c001a000c001a000c0040000c0040000c05f4"],  # VolDown
                [b"\x00\xa4", "0221017c0020123c000c001a000c0040000c001a000c001a000c001a000c001a000c001a000c001a000c001a000c0040000c0040000c0040000c0040000c001a000c001a000c05f4000c001a000c0040000c001a000c001a000c001a000c0040000c0040000c0040000c0040000c001a000c001a000c001a000c001a000c0040000c0040000c05f4"],  # Mute
                [b"\x00\x1a", "0221017c0020123c000c001a000c0040000c001a000c001a000c001a000c0040000c001a000c001a000c001a000c001a000c001a000c0040000c0040000c001a000c001a000c05f4000c001a000c0040000c001a000c001a000c001a000c001a000c0040000c0040000c0040000c0040000c0040000c001a000c001a000c0040000c0040000c05f4"],  # Power
                [b"\x00\xb2", "0321017c00220002015700ab0016001600160016001600410016001600160016001600160016001600160016001600410016004100160016001600410016004100160041001600410016004100160016001600160016001600160041001600160016001600160016001600160016004100160041001600410016001600160041001600410016004100160041001605f50157005600160e60"],  # InputSelect
            ]

            print("Programming mode on.")
            await program_start(client)

            for key, value in codes_to_program:
                await program_code(client, key, value)

            await program_stop(client)
            print("Programming complete.")

    except BleakError as e:
        print(f"Error BLE: {e}")
    except Exception as e:
        print(f"Error: {e}")


# -------------------------------
# Start here
# -------------------------------
async def main():
    # If no MAC option, select from scanning
    if len(sys.argv) < 2:
        print("Scanning (10 seconds)...")
        devices = await BleakScanner.discover(timeout=10.0)
        for i, d in enumerate(devices):
            print(f"[{i}] {d.name or '(noname)'} — {d.address}")

        if not devices:
            print("no BLE devices.")
            return

        idx = int(input("Type device number: "))
        address = devices[idx].address
    else:
        address = sys.argv[1]

    await run(address)


if __name__ == "__main__":
    asyncio.run(main())
