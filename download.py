import feedparser
import Crowbars

from os import environ

feed_data = feedparser.parse(environ["CANVASSYNC_FEED"])
Crowbars.log("Loaded Canvas entries. Found " + str(len(feed_data.entries)) + ".")

saved_entry_ids = Crowbars.get_saved_entry_ids()
Crowbars.log("Loaded Saved entries. Found " + str(len(saved_entry_ids)) + ".")

session = Crowbars.perform_sso_login(environ["CANVASSYNC_SSO_USERNAME"], environ["CANVASSYNC_SSO_PASSWORD"], environ["CANVASSYNC_SSO_URL"])
Crowbars.log("Logged in.")

for entry in feed_data.entries:
    if entry.id not in saved_entry_ids:
        Crowbars.download_entry(session, entry)
        Crowbars.save_entry_id(entry.id)