import logging
import os

from slack_bolt import App, BoltContext
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.webhook import WebhookClient

# Database models
from .models import SlackInstallation
from django.db.models import F

# Bolt datastore implementations
from .slack_datastores import DjangoInstallationStore, DjangoOAuthStateStore

logger = logging.getLogger(__name__)
client_id, client_secret, signing_secret, scopes = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
    os.environ.get("SLACK_SCOPES", "commands").split(","),
)

app = App(
    signing_secret=signing_secret,
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
        # If you want to test token rotation, enabling the following line will make it easy
        token_rotation_expiration_minutes=1000000,
        installation_store=DjangoInstallationStore(
            client_id=client_id,
            logger=logger,
        ),
        state_store=DjangoOAuthStateStore(
            expiration_seconds=120,
            logger=logger,
        ),
    ),
)
#########################################################################################
# import logging
# import os

# from slack_bolt import App, BoltContext
# from slack_bolt.oauth.oauth_settings import OAuthSettings
# from slack_sdk.webhook import WebhookClient

# # Database models
# from .models import SlackInstallation
# from django.db.models import F

# # Bolt datastore implementations
# from .slack_datastores import DjangoInstallationStore, DjangoOAuthStateStore

# import os
# from slack import WebhookClient
# from slack_bolt import App, BoltContext
# from slack_bolt.oauth.oauth_settings import OAuthSettings
# from slack_sdk.oauth.installation_store import FileInstallationStore
# from slack_sdk.oauth.state_store import FileOAuthStateStore
# from django.db.models import F

# from .models import SlackInstallation

# oauth_settings = OAuthSettings(
#     client_id=os.environ["SLACK_CLIENT_ID"],
#     client_secret=os.environ["SLACK_CLIENT_SECRET"],
#     scopes=["channels:read", "groups:read", "chat:write"],
#     installation_store=FileInstallationStore(base_dir="./data/installations"),
#     state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states")
# )

# app = App(
#     signing_secret=os.environ["SLACK_SIGNING_SECRET"],
#     oauth_settings=oauth_settings
# )
############################################################################################33

def event_test(body, say, context: BoltContext, logger):
    logger.info(body)
    say(":wave: What's up?")

    found_rows = list(
        SlackInstallation.objects.filter(enterprise_id=context.enterprise_id)
        .filter(team_id=context.team_id)
        .filter(incoming_webhook_url__isnull=False)
        .order_by(F("installed_at").desc())[:1]
    )
    if len(found_rows) > 0:
        webhook_url = found_rows[0].incoming_webhook_url
        logger.info(f"webhook_url: {webhook_url}")
        client = WebhookClient(webhook_url)
        client.send(text=":wave: This is a message posted using Incoming Webhook!")


# lazy listener example
# def noop():
#     pass


# app.event("app_mention")(
#     ack=event_test,
#     lazy=[noop],
# )

@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")

@app.command("/hello-django-app")
def command(ack):
    ack(":wave: Hello from a Django app :smile:")
