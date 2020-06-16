# Virtual Tabletop
A simple interface for virtualizing game boards and displaying on a table monitor.

# Purpose
This application is intended to interface with an off-site database to download and display user-created game boards onto television-integrated tables. This allows equipped tables to facilitate gameplay without requiring physical game pieces or boards.

Users can designate a firebase realtime database to pull from, upload game boards along with proper dimensions, and download them for play. The application will handle converting and compressing files as well as properly scaling them on the designated board screen.

An example use would be for a tabletop RPG, such as D&D. A dungeon master could upload boards ahead of a session and could simply display the next encounter without wasting precious time fiddling with tiles. This promotes secrecy, coherency, and board reuse.

# Realtime Database
Due to the lack of an official or supported client-side firestore model, this application uses firebase realtime database. As such, it is limited to a JSON depth of 32, which limits collections. Therefore, collections are currently only supported to a depth of 2. Future plans might be made to group by reference in order to have more logical groupings, but this might complicate local storage. Additionally, additional use of firebase storage will be required for file hosting, so a preview image field is added to the game structure in order to minimize network traffic and ram usage for the intended environment. Users should be sure to upload a compressed image or thumbnail for this.

# Environment
This application requires Python 3.x as well as an internet connection and is intended for a dual-screen Raspberry Pi. It assumes the main screen is a hidden screen to be used by the game master and the second screen is an upward-facing monitor inlaid into a table. The primary screen is used to select and close game boards.
