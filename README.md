# calendar\_sync
Scripts to automate copying OS X Calendar events into a different calendar.

## What is it?
`calendar_sync` is a utility that copies the next `n` days of calendar events from one calendar into another.  This can
be useful for keeping iCloud and Non-iCloud calendars in sync.

## How it works
* First, it gets a summary of the next `n` days of calendar events in Automator.
* Second it calls a Python script to sync those calendar events to the destination calendar.
* The Python script deletes all events in the destination calendar.  **I repeat, the python script deletes all events
 in the destination calendar**.
* The Python script then creates a new event in the destination calendar for each event in the summary.

## Setup
### First, a word of WARNING!
* The destination calendar that is chosen in the Python script will be deleted.  **ALL calendar events in the calendar
 with that name will be deleted**.  There is no warning, and no way to undo this.
* You have been warned.

### Python Script
* Adjust the destination calendar in the python script.  Choose wisely since all events in this calendar will be
deleted.
* Adjust any filtered event summaries.
* Set the `dry_run` setting.  If `dry_run` is True then calendar changes are logged but not applied.  It is best to
set `dry_run` to True while getting things working for the first time.
* Set the `include_descriptions` setting.  Setting `include_descriptions` to False will prevent the calendar entry
descriptions from being copied.

### Automator Script
* The automator script can edited by opening the calendar_sync.workflow in Automator.
* Adjust the source calendar name to the calendar you want to sync from.
* Choose the timeframe for events to sync.
* Adjust the `Run shell script` command to point to the location of the Python script, and to write the log to a
desired location.
* Save the script.

### Calendar
* Create a new Calendar in the OS X Calendar application to contain the sync'd calendar events.  In case you somehow
missed it above, **ALL of the events in this calendar will be deleted every time the `calendar_sync` is run.**

### Try it out
The Automator script can be run in the Automator application.  The output from the Python script can be seen in the
Results tab of the `Run Shell Script` Action.
At this point you should have a copy of the events from the source calendar in the destination calendar.

### Schedule the Automator script
The best way to schedule the sync is via cron.
Run 'crontab -e'
Add an entry such as:

```30 6,10,16,20 * * * automator /Users/Wally/scripts/calendar_sync.workflow```

Save the changes.
The first time the sync runs, you will need to grant access to your calendar to `cron`.

## Usage
That's about it.  If everything is working as expected, there will always be `n` days of calendar events synchronized
from the source calendar to the destination calendar.  Enjoy.
