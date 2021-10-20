# Drapetisca

A sample multiplayer game using Astra Streaming, FastAPI, React and Websockets


## Barebones steps

### Astra setup

### Gitpod

(Ctrl+)Click [this](https://gitpod.io/#https://github.com/hemidactylus/drapetisca)
to open this project in Gitpod. Then wait a few minutes.

Gitpod starts with two shells open: api and client, "almost" ready to go. We will have stuff running on both.

#### API shell

Create a file `.env` by copying the `.env.sample` in the same directory and filling it with values found
on your Astra Streaming "Connect" tab:

- `SERVICE_URL`: it looks like `pulsar+ssl://pulsar-aws-useast2.streaming.datastax.com:6651`
- `ASTRA_TOKEN`: to get it, you have to click "Show" on that same page. Guard this as a secret!

Make sure you are in the API shell.
Make these environment variables available to the shell by typing:

    . ../.env

_Explanations on how the API works..._

Launch the API with:

    uvicorn api:app --reload

you will see the API start, happily ready to accept requests. Leave it run

#### Client shell

Switch to the client shell. We took care of preinstalling all required dependencies for you.

You simply have to start the client, which will open in the "simple browser" within Gitpod.

#### Play the game!

