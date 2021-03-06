"""bot1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Set this flag to False if you want to enable oauth_app instead
is_simple_app = False

if is_simple_app:
    # A simple app that works only for a single Slack workspace
    # (prerequisites)
    # export SLACK_BOT_TOKEN=
    # export SLACK_SIGNING_SECRET=
    from simpleApp.urls import slack_events_handler

    urlpatterns = [path("slack/events", slack_events_handler)]
else:
    # OAuth flow supported app
    # (prerequisites)
    # export SLACK_CLIENT_ID=
    # export SLACK_CLIENT_SECRET=
    # export SLACK_SIGNING_SECRET=
    # export SLACK_SCOPES=app_mentions:read
    #token scopes
    #xapp-1-A037M9EC23C-3272544026150-2fcdc3da99d566d2cab2e0c179ce63c0df89efd46aa544f458b7cd86f037d402
    from slackbot.urls import slack_events_handler, slack_oauth_handler

    urlpatterns = [
        path("slack/events", slack_events_handler, name="handle"),
        path("slack/install", slack_oauth_handler, name="install"),
        path("slack/oauth_redirect", slack_oauth_handler, name="oauth_redirect"),
    ]