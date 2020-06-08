# Virtual Tabletop
A simple interface for virtualizing game boards and displaying on a table monitor.

# Purpose
This application is intended to interface with an off-site database to download and display user-created game boards onto television-integrated tables. This allows equipped tables to facilitate gameplay without requiring physical game pieces or boards.

Users can designate a firebase database to pull from, upload game boards along with proper dimensions, and download them for play. The application will handle converting and compressing files as well as properly scaling them on the designated board screen.

an example use would be for a tabletop RPG, such as D&D. A dungeon master could upload boards ahead of a session and could simply display the next encounter without wasting precious time fiddling with tiles. This promotes secrecy, coherency, and board reuse.

# Environment
This application requires Python 3.x as well as an internet connection and is intended for a dual-screen Raspberry Pi. It assumes the main screen is a hidden screen to be used by the game master and the second screen is an upward-facing monitor inlaid into a table. The primary screen is used to select and close game boards.
