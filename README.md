Pomegranate-Note_Taker
======================

Web page [http://pomegranate-pkm.org/archives/41](http://pomegranate-pkm.org/archives/41)

Pomegranate Note Taker is a small note taker and screen capture desktop application that complements Pomegranate PKM web application. It written in Python and its GUI in PyQt4.

It does three things:

* Saving or appending the text entered in the text area to a plain text file
* Capturing the full screen either manually (from menu or Ctrl+S)
* It reminds and prompts the user to capture the screen in case an important work is done and would like to take a journal entry of what was done at that particular time. The interval of prompting the user is set in the script. Currently 15 minutes.

## Details

The filename is determined according to the first word of the text. If it is one-letter work (e.g. t for Task), the text is appending to the file named T-dd.MM.yy.txt where dd.MM.yy is today's date.

If the first word is of more than one letter, the text is saved in a new file named first_word-dd.MM.yy_HH-mm-ss.txt, where the datetime is that of the save operation.

When capturing the desktop, the text entered is also saved in the picture IPTC metadata title field. Also it is appended to a special file. This is to ensure the text is saved even if it too long or contains characters that are illegal for filename e.g. < > / etc. The filename is limited to the first 80 characters and the illegal characters replaced by underscore.

The script is currently 290 lines long. It is available at this link: pomegranate-note_taker_3.1

 

 