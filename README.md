# calendar\_sync
Scripts to automate copying OS X Calendar events into a different calendar.

## What is it?
calendar\_sync is a utility that copies the next 'n' days of calendar events from one calendar into another.  This can be useful for keeping iCloud and Non-iCloud calendars in sync.

## How it works
* First, it gets a summary of the next 'n' days of calendar events in Automator.
* Second it calls a Python script to sync those calendar events to the destination calendar.
* The Python script deletes all events in the destination calendar.  I repeat, the python script deletes all events in the destination calendar.
* The Python script then creates a new event in the destination calendar for each event in the summary.

## Setup
### First, a word of WARNING!
* The destination calendar that is chosen in the Python script will be deleted.  ALL calendar events
in the calendar with that name will be deleted.  There is no warning, and no way to undo this.
* You have been warned.

### Python Script
* Adjust the destination calendar in the python script.  Choose wisely since all events in this calendar will be deleted.
* Adjust any filtered event summaries.
* Set the dry\_run setting.  If dry\_run is True then calendar changes are logged but not applied.  It is best to set dry\_run to True while getting things working for the first time.
* Set the include\_descriptions setting.  Setting include\_descriptions to False will prevent the calendary entry descriptions from being copied.

### Automator Script
* Move the Automator script to your iCloud drive under the Automator folder.
* Adjust the source calendar name to the calendar you want to sync from.
* Choose the timeframe for events to sync.
* Adjust the 'Run shell script' command to point to the location of the Python script, and to write the log to a desired location.
* Choose 'File->Convert To...' in Automator.  Choose 'Calendar Alarm'.
* Choose 'File->Save...' in Automator.  Enter 'Calendar Sync' as the name.
* When you save the script, Automator will ask for access to your Calendar.  A new 'Automator' calendar will be created in the 'On My Mac' section of Calendar.  This will be used to automate running the script.  See 'Schedule the Automator script' below.

### Calendar
* Create a new Calendar in the OS X Calendar application to contain the sync'd calendar events.  In case you somehow missed it above, ALL of the events in this calendar will be deleted every time the calendar\_sync is run.

### Try it out
The Automator script can be run in the Automator application.  The output from the Python script can be seen in the Results tab of the 'Run Shell Script' Action.
At this point you should have a copy of the events from the source calendar in the destination calendar.

### Schedule the Automator script
A new 'Automator' calendar should have been created in the 'On My Mac' Calendar section when you saved the Automator script.  There should also be a single event called 'Calendar Sync'.
That event should have an 'Open File' alert that will open the Calendar Sync automator script.

Adjust the Repeat settings for the calendar event to schedule the synchronizations.  The event can be copied to have it run multiple times a day.

To avoid Notification Center updates in OS X, right-click on the Automator calendar, choose 'Get Info', and choose 'Ignore Events'.

## Usage
That's about it.  If everything is working as expected, there will always be 'n' days of calandar events synchronized from the source calendar to the destination calendar.  Enjoy.
