# rocketchat-google-calendar
Integration of rocketChat with Google calendar using a python script to create a webhook

The solution consists of two parts. 
1. A python script that connects to google calendar API and sends the data to RocketChat
2. An incoming webhook in RocketChat that interprets the data sent from the python script


## Instructions
1. Checkout the project
1. Create an incoming webhook in your RocketChat
  1. Go to RocketChat-> Administration-> Integrations-> New Integration-> Incoming webhook
  1. Set "Enabled" to "true"
  1. Give a name for the webhook
  1. Define the channel you want the events to appear (ex: #calendar-events). Make sure the channel exists
  1. Set "Script Enabled" to "true"
  1. Put in the script field the contents of the file webhook.js
  1. Press "save changes"
  1. Copy the contents of the newly created field "Webhook URL" to clipboard. You will need it.
1. Configure the python script
  1. Open the file calendarWebhook.py
  1. On line 18, put the url you copied form the RocketChat incoming webhook
  1. Open in your browser your google calendar, find the settings of that specific calendar and copy the CalendarId
  1. Paste the CalendarId on line 21
  1. If you want your results to appear in a specific timezone, fill in the line 24 (example: Europe/Athens)
1. Install python prerequisites 
  1. pip install --upgrade google-api-python-client
  1. pip install requests
1. Create google api credentials as shown at: https://developers.google.com/google-apps/calendar/quickstart/python (step 1)
1. Put client_secret.json from above step in the same directory  as your python scrpt
1. Fire up the OAuth authentication process by running it once on shell/terminal 
  1. Create an event in your calendar starting somewhere in the next 30 minutes
  1. run:  python calendarWebhook.py
  1. follow the instructions for authorising the script to access the calendar. Note: The user you use to authorise should have access to the calendar
  1. If all went well, it should post the calendar event in your channel
1. set to run every 5 minutes