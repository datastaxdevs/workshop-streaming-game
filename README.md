# Drapetisca

A sample multiplayer game using Astra Streaming, FastAPI, React and Websockets


## Barebones steps

### Astra setup

#### Create your Astra DB instance

the usual. At the moment the DB is not even used (but we have to create it anyway).

#### Create your Astra Streaming

Now it's time to create a new Astra Streaming topic, that will convey all messages
for this app.

- Go to your Astra console, locate the "Create Streaming" button on the left and click on it
- Set up a new Tenant (remember Pulsar has a multi-tenant architecture): call it `gameserver` and pick the provider/region you like. Hit "Create Tenant"
- You'll shortly see the dashboard for your newly-created Tenant. Go to the "Topics" tab to create a new one (we will stay in the "default" namespace)
- In the "Topics" tab, click "Add Topic" and name it `worldupdates` (persistent = yes, partitioned = no). Click "Save" to confirm topic creation

> Note: technically you can name your tenant, namespace and topic anything you want - but then you have to make sure the settings in your API code are changed accordingly.

- <details><summary>Show me the steps</summary>
    <img src="https://github.com/hemidactylus/drapetisca/raw/main/images/astra_create_streaming_topic.gif?raw=true" />
</details>

While we are at it, let's have a look at the information needed to connect to the topic
from the API code. While still in the tenant dashboard, find the "Connect" tab and click on it: you will see a listing of "Tenant Details".
You will later need the "Broker Service URL" and the "Token" values (the latter is hidden but can be copied nevertheless).

Your topic is created almost in real-time, ready to receive and dispatch a stream of messages that will make your game work!
Time to prepare some code to be run...

### Gitpod

(Ctrl+)Click [this](https://gitpod.io/#https://github.com/hemidactylus/drapetisca)
to open this project in Gitpod. Then wait a few minutes.

_What does this Gitpod click do? ..._

Gitpod starts with two shells open: api and client, "almost" ready to go. We will have stuff running on both.

#### API shell

Create a file `.env` by copying the `.env.sample` in the same directory and filling it with values found
on your Astra Streaming "Connect" tab:

- `SERVICE_URL`: it looks like `pulsar+ssl://pulsar-aws-useast2.streaming.datastax.com:6651`
- `ASTRA_TOKEN`: a very long (about 500 chars) string of characters. To view it, click "Show" on that same page. Guard your token as a secret!

Make sure you are in the API shell.
Make these environment variables available to the shell by typing:

    . ../.env

_Explanations on how the API works..._

Launch the API with:

    uvicorn api:app --reload

you will see the API start, happily ready to accept requests. Leave it run

#### Client shell

Switch to the client shell. We took care of preinstalling all required dependencies for you.

Nevertheless, let us ensure all dependencies are installed:

    npm install

Now you simply have to start the client, which will open in the "simple browser" within Gitpod:

    npm start

If you are running everything locally on your computer, you would be able
to open the client on `http://localhost:3000` at this point and use the
default API location of `ws://localhost:8000` to enter the game.

However, we are working within Gitpod, which wraps locally-exposed ports
and makes them potentially accessible over the Internet.
Have a look at the address bar
in Gitpod's simple browser: it has been automatically converted from the
above `localhost` address to something such as
`https://3000-tan-swallow-2yz174hp.ws-eu17.gitpod.io`.

_Explanations on how the client works ..._

#### Play the game!

We have a client and an API ready to accept (Websocket) connections:
it is time to play!

The client lets you customize your player name and gives you a unique player ID.

It also needs the address to reach the API. Now, if you are running locally you
would be good to go, but since we are working within Gitpod you have to adapt
the "API Location" to reflect the Gitpod-provided domain.

You can either run the command `gp url 8000 | sed s/https/wss/` and copy
the output or simply take the client address as in the example above and replace
`3000` with `8000` (the API listen on port 8000), and `https` with `wss`
(we are using the secure Websocket protocol). Your API Location will look
something like:

    wss://8000-tan-swallow-2yz174hp.ws-eu17.gitpod.io

You can finally click "Enter game". At this point the client establishes
Websocket connections to the API, after which you will see your player appear
in the center of the arena.

Try to move the player with the arrow buttons: you can control your movements
in the game!

Now try to go beyond the boundaries of the arena: what happens? We purposefully
left all checks out of the client (which blindly increases/decreases your X and Y
coordinates) to demonstrate that the checks and validation occurs on the API layer.
It is the API that sends updates on the world state back to the client, and
rightly so -- think about cheaters in online games!

But this is a _multiplayer_ game, isn't it? So Let us simply open a new
browser tab and enter the same client URL as above (the one on port 3000).
Enter a different player name and the same API Location you built above, then
hit "Enter Game". Hooray! As soon as you move around with this new player,
you will see the whole architecture at work:

- client sends updates on your player's position through the "player websocket"
- API validates this update and writes it to the Astra Streaming topic
- API receives new messages by listening to this same Astra Streaming topic
- API broadcasts updates on any player to all connected clients through the "world websocket"
- at each such update, the client's game arena is adjusted

What is really cool is that you can give this URL to your friends and have them
enter your very own multiplayer game!

_Please do this and tell the world about how easy it is to build a multiplayer real-time
game with Astra Streaming!_

#### Fun with the Streaming UI

(manually connecting to the topic in the Astra Streaming UI and seeing the messages pour in)

(then, sending a crafted message pretending to be a player update and see the effect on the gameplay!)

#### Finally

Now let me give you all MY address and let us run like crazy around my arena!

"Now form a circle shape! Now a smiley..."
