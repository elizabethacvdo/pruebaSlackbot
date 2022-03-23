import logging
import os

from slack_bolt import App, BoltContext, Say
from slack_bolt.oauth.oauth_settings import OAuthSettings



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
    # token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=signing_secret,
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
       # token_verification_enabled=False,
        # If you want to test token rotation, enabling the following line will make it easy
        # token_rotation_expiration_minutes=1000000,
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
# app.client.oauth_v2_access

# def event_test(body, say, context: BoltContext, logger):
#     logger.info(body)
#     say(":wave: What's up?")

#     found_rows = list(
#         SlackInstallation.objects.filter(enterprise_id=context.enterprise_id)
#         .filter(team_id=context.team_id)
#         .filter(incoming_webhook_url__isnull=False)
#         .order_by(F("installed_at").desc())[:1]
#     )
#     if len(found_rows) > 0:
#         webhook_url = found_rows[0].incoming_webhook_url
#         logger.info(f"webhook_url: {webhook_url}")
#         client = WebhookClient(webhook_url)
#         client.send(text=":wave: This is a message posted using Incoming Webhook!")

# def noop():
#     Say("hola")


# app.event("app_mention")(
#     ack=event_test,
#     lazy=[noop],
# )


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")

@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")

#########################################################################################
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 8000)))