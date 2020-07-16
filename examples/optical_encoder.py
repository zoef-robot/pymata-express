"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import asyncio
import sys
from pymata_express.pymata_express import PymataExpress

# This program continuously monitors an optical encoder sensor
# It reports changes to the distance sensed.


# A callback function to display the distance
async def the_callback(data):
    """
    The callback function to display the change in encoder value
    :param data: [pin_type=23, pin number, value, timestamp]
    """
    print("Encoder value: ", data[0])


async def optical_encoder(my_board, pin_nr, wheel_size=20, interrupt_mode=2, callback=None):
    """
    Set the pin mode for a sonar device. Results will appear via the
    callback.

    :param my_board: an pymata express instance
    :param pin_nr: Arduino pin number
    :param callback: The callback function
    """

    # set the pin mode for the trigger and echo pins
    await my_board.set_pin_mode_optenc(pin_nr, wheel_size, interrupt_mode, callback)

    # wait forever
    while True:
        try:
            await asyncio.sleep(2)
            print(await my_board.optenc_read(pin_nr))
        except KeyboardInterrupt:
            await my_board.shutdown()

loop = asyncio.get_event_loop()
board = PymataExpress()
try:
    loop.run_until_complete(optical_encoder(board, pin_nr=15, callback=the_callback))
    loop.run_until_complete(board.shutdown())
except (KeyboardInterrupt, RuntimeError):
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
