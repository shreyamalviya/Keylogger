# Keylogger
A keylogger for Linux in Python

Once the script starts, all key presses are logged into an output file, until the script is stopped.

EDIT: All keypresses are emailed to specified address (default: self) depending on entered buffer size.

# Design

The following diagram describes the general mechanism for fetching the event info for a device.

<img src="images/design.png" width="500">

Currently, only fetching event info for the keyboard is supported. 
