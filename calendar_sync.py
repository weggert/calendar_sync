#!/usr/bin/python
import fileinput
import os


class CalendarManager:

    def __init__(self, calendar_name, dry_run, include_descriptions):
        self.calendar_name = calendar_name
        self.dry_run = dry_run
        self.include_descriptions = include_descriptions

    def clear_calendar(self):
        command = """
osascript -e 'tell application "Calendar" to tell calendar "%s"
  set eventList to every event
  repeat with e in eventList
    delete e
  end repeat
end tell'
"""
        command = command % self.calendar_name

        if not self.dry_run:
            os.system(command)
        print 'Calendar cleared'
        
    def create_calendar_event(self, summary, start_date, end_date, all_day, location, description):
        if not self.include_descriptions:
            description = ''

        properties = 'start date:theStartDate, end date:theEndDate, summary:"%s", description:"%s", location:"%s"'\
                     % (summary, description, location)
        if all_day is True:
            properties += ', allday event:true'
        command = """
osascript -e 'set theStartDate to date "%s"
set theEndDate to date "%s"
tell application "Calendar" to tell calendar "%s"
   set theEvent to make new event with properties {%s}
end tell'
"""
        command = command % (start_date, end_date, self.calendar_name, properties)

        if not self.dry_run:
            os.system(command)
        self.print_summary(summary, start_date, end_date, all_day, location, description)

    @staticmethod
    def print_summary(summary, start_date, end_date, all_day, location, description):
        print 'Summary: ' + summary
        print '  Start: ' + start_date
        print '  End: ' + end_date
        print '  All Day: ' + str(all_day)
        print '  Location: ' + location
        print '  Description: ' + description
        print ''


class CalendarSummaryProcessor:

    class LineType:
        EventStart, Summary, Location, Date, Time, Where, Notes, Status, Other = range(9)

        def __init__(self):
            pass

    def __init__(self, calendar_name, dry_run, include_descriptions):
        self.calendar_manager = CalendarManager(
            calendar_name=calendar_name,
            dry_run=dry_run,
            include_descriptions=include_descriptions)
        self.reset()
        self.processing_event = False
        self.first_description_line = True
        self.last_description_line_was_blank = False
        self.summary = ''
        self.date = ''
        self.time = ''
        self.location = ''
        self.description = ''

    def reset(self):
        self.processing_event = False
        self.first_description_line = True
        self.last_description_line_was_blank = False
        self.summary = ''
        self.date = ''
        self.time = ''
        self.location = ''
        self.description = ''

    def process_summary(self):
        self.calendar_manager.clear_calendar()

        for input_line in fileinput.input():
            line_type = self.get_line_type(input_line)

            if line_type is self.LineType.EventStart:
                if self.processing_event:
                    if self.summary != 'Remote'\
                        and self.summary != 'IP Video - Daily Scrum'\
                            and self.summary != 'Cloud Team Scrum':
                                start_date, end_date, all_day = self.get_start_end_dates(self.date, self.time)
                                self.calendar_manager.create_calendar_event(
                                    self.summary, start_date, end_date, all_day, self.location, self.description)
                self.reset()

            if line_type is self.LineType.Summary:
                self.summary = self.sanitize_line(input_line.strip()[9:])
                self.processing_event = True

            if line_type is self.LineType.Date:
                self.date = input_line.strip()[6:]

            if line_type is self.LineType.Time:
                self.time = input_line.strip()[6:]

            if line_type is self.LineType.Location:
                self.location = self.sanitize_line(input_line.strip()[10:])
                self.processing_event = True

            if line_type is self.LineType.Other:
                description_line = self.sanitize_line(input_line.strip())
                if len(description_line) > 0:
                    self.description = self.description + description_line + '\n'
                    self.last_description_line_was_blank = False
                else:
                    if not self.first_description_line and not self.last_description_line_was_blank:
                        self.description += '\n'
                    self.last_description_line_was_blank = True
                self.first_description_line = False

        if self.processing_event:
            start_date, end_date, all_day = self.get_start_end_dates(self.date, self.time)
            self.calendar_manager.create_calendar_event(
                self.summary, start_date, end_date, all_day, self.location, self.description)

    @staticmethod
    def get_start_end_dates(date, time):
        dates = date.split(" to ")
        times = time.split(" to ")
        start_date = dates[0] + ' ' + times[0]
        end_date = dates[1] + ' ' + times[1]
        all_day = False
        if times[0] == '12:00:00 AM' and times[1] == "12:00:00 AM" and dates[0] != dates[1]:
            all_day = True
        return start_date, end_date, all_day

    def get_line_type(self, input_line):
        if input_line.startswith('EVENT'):
            return self.LineType.EventStart

        if input_line.startswith('Summary:'):
            return self.LineType.Summary

        if input_line.startswith('Date:'):
            return self.LineType.Date

        if input_line.startswith('Time:'):
            return self.LineType.Time

        if input_line.startswith('Location:'):
            return self.LineType.Location

        if input_line.startswith('Where'):
            return self.LineType.Where

        if input_line.startswith('Notes'):
            return self.LineType.Notes

        if input_line.startswith('Status'):
            return self.LineType.Status

        return self.LineType.Other

    def process_named_line(self, input_line):
        colon_position = input_line.find(':')
        return self.sanitize_line(input_line[colon_position+1:].strip())

    @staticmethod
    def sanitize_line(input_line):
        return input_line.replace("'", "").replace('"', '').replace('*~*~*~*~*~*~*~*~*~*', '').strip()


CalendarSummaryProcessor(calendar_name='Work Calendar',
                         dry_run=False,
                         include_descriptions=True).process_summary()