# Anvur Journal app

Anvur is the Italian entity providing abilitations for Associate and Full University Professors in Italy. Each applicant needs to have a certain number of works published on scientific journals listed by Anvur in its scientific sector in order to be successful.

The aim of this app is to facilitate search of journals listed by Anvur and provide additional information from Scimago Journal Rank. This app is divided into two components: server and client.

Live demo at [https://anvur.pages.dev/](https://anvur.pages.dev/).

## Server
The server downloads and parses PDF files from Anvur website to extract and structure information about journals.

## Client
The client app has bundled data from Anvur and performs searches on its journal database. It can also fetch and structure information from Scimago JR to enrich the information available. It can connect to the server to update its information from Anvur.
