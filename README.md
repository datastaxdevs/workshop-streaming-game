<!--- STARTEXCLUDE --->
# Drapetisca: a multiplayer online game with Astra Streaming and Websockets

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/datastaxdevs/workshop-streaming-game)
[![License Apache2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Discord](https://img.shields.io/discord/685554030159593522)](https://discord.com/widget?id=685554030159593522&theme=dark)

Time: *50 minutes*. Difficulty: *Intermediate*. [Start Building!](#lets-start)

A simple multiplayer online game featuring
* Astra Streaming (built on top of Apache Pulsar)
* WebSockets
* React.js for the front-end
* the Python FastAPI framework for the back-end

<!--- ENDEXCLUDE --->

![Drapetisca screenshot](images/drapetisca_intro.png)

## Objectives
* Understand the architecture of a streaming-based application
* Learn how Apache Pulsar works
* Learn about Websockets on client- and server-side
* Understand how a FastAPI server can bridge Pulsar topics and WebSockets
* Understand the structure of a Websocket React.js application
* **get your very own online gaming platform to share with your friends!**

## Frequently asked questions

- *Can I run the workshop on my computer?*

> There is nothing preventing you from running the workshop on your own machine.
> If you do so, you will need
> * git installed on your local system
> * [node 15 and npm 7 or later](https://www.whitesourcesoftware.com/free-developer-tools/blog/update-node-js/)
> * [Python v3.8+ installed on your local system](https://www.python.org/downloads/)
>
> In this readme, we try to provide instructions for local development as well - but keep in mind that
> the main focus is development on Gitpod, hence **We can't guarantee live support** about local development
> in order to keep on track with the schedule. However, we will do our best to give you the info you need to succeed.

- *What other prerequisites are there?*
> * You will need a GitHub account
> * You will also need an Astra account: don't worry, we'll work through that in the following

- *Do I need to pay for anything for this workshop?*
> * **No.** All tools and services we provide here are FREE.

- *Will I get a certificate if I attend this workshop?*

> Attending the session is not enough. You need to complete the homeworks detailed below and you will get a nice badge.

- *Why "Drapetisca"?*

> _Drapetisca socialis_, known as "invisible spider", is a very small and hard-to-notice spider found throughout Europe.
> Since this is a multiplayer game that lets players have social interactions in the play area, why not choose a spider
> with "socialis" in its name?

## Materials for the Session

It doesn't matter if you join our workshop live or you prefer to work at your own pace,
we have you covered. In this repository, you'll find everything you need for this workshop:

- [Slide deck](slides/DataStaxDevs-workshop-Build_a_Multiplayer_Game_with_Streaming.pdf)
- [Discord chat](https://bit.ly/cassandra-workshop)
- [Questions and Answers](https://community.datastax.com/)

## Homework

<img src="images/streaming-workshop.png?raw=true" width="200" align="right" />

Don't forget to complete your assignment and get your verified skill badge! Finish and submit your homework!

1. Complete the practice steps as described below until you have your own app running in Gitpod.
2. Now roll up your sleeves and modify the code in two ways: (1) we want the API to send a greeting to each new player in the chat box, and (2) we want the player names in the game area to match the icon color. _Please read the detailed guidance found [below](#6-homework-instructions)_.
3. Take a SCREENSHOT of the running app modified this way. _Note: you will have to restart the API and reload the client to see all changes!_
4. Submit your homework [here](https://dtsx.io/streaming-game-homework).

That's it, you are done! Expect an email in a few days!

# Let's start

## Table of contents

1. [Create your Astra Streaming instance](#astra-setup)
2. [Load the project into Gitpod](#2-load-the-project-into-gitpod)
3. [Set up/start the API](#3-api-setup)
4. [Set up/start the client](#4-client-setup)
5. [Play!](#5-play-the-game)
6. [Homework instructions](#6-homework-instructions)
7. [Selected topics](#7-selected-topics)

## Astra setup

### 1. Create your Astra Streaming instance

> **`No Astra database` today**: we won't be instantiating a database (unlike
> most of our workshops); we will be exclusively using "Streaming" instead.

_**`Astra Streaming`** is the simplest way to get a streaming infrastructure based on Apache Pulsar
with zero operations at all - just push the button and get your streaming.
No credit card required - with the free tier comes a generous monthly-renewed credit for you to use._

_**`Astra Streaming`** is tightly integrated with `Astra DB`, the database-as-a-service
used in most of our other workshops. **If you already have an Astra DB account, you can use that
one in the following!**_

For more information on Astra Streaming, look at [the docs](https://docs.datastax.com/en/astra-streaming/docs/).
For more information on Apache Pulsar, here is [the documentation](https://pulsar.apache.org/docs/en/concepts-overview/).

#### 1a. Register

Register and sign in to Astra at `https://astra.datastax.com` by clicking this button (better in a new tab with Ctrl-click or right-click):

<a href="https://astra.dev/11-17"><img src="images/create_astra_button.png" /></a>

_you can use your `Github`, `Google` accounts or register with an `email`.
Choose a password with minimum 8 characters, containing upper and lowercase letters, at least one number and special character.
You may be asked to verify your email, so make sure you have access to it._

<details><summary>Show me the steps</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/astra_signup.gif?raw=true" />
</details>

#### 1b. Create streaming

Once registered and logged in, you will be able to create a streaming topic for use in this workshop.

> Heads up! Astra lets you also create Databases in the cloud (based on Apache Cassandra); in this workshop we will not need to,
> but keep that in mind. You can also effortlessly connect your streaming topics and an Astra DB instance to enrich your app!

Now it's time to create a new Astra Streaming topic, that will convey all messages for this app.

- Go to your Astra console, locate the "Create Streaming" button on the left window and to the right of Streaming. Click on it.
- Set up a new Tenant (remember Pulsar has a multi-tenant architecture): _you have to find a globally unique name for it_,
so for instance if `gameserver` is already taken by someone, try `gameserver0`, `gameserver-abc` or something similar.
Pick the provider/region you like (_try to have it close to you for reduced latency_) and finally hit "Create Tenant". **Remember the name of your tenant for the API setup step later**.
- You'll shortly see the dashboard for your newly-created Tenant. Go to the "Topics" tab to create a new one (we will stay in the "default" namespace).
- In the "Topics" tab, click "Add Topic" and name it `worldupdates` (persistent = yes, partitioned = no). Click "Save" to confirm topic creation.

Congratulations! Your topic is being created, which takes less than one minute, and is now ready to receive and
dispatch the stream of messages that will make your game work!

> Note: technically you can name your namespace and topic anything you want - but then you have to make sure
> the environment settings for your API code are changed accordingly (see later).

<details><summary>Show me the steps</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/astra_create_streaming_topic.gif?raw=true" />
</details>

#### 1c. Check connection details

While you are at it, have a look at the information needed to connect to the topic
from the API code. While still in the tenant dashboard, find the "Connect" tab and click on it: you will see a listing of "Tenant Details".
You will later need the "Broker Service URL" and the "Token" values (the latter is hidden but can be copied nevertheless).

<details><summary>Show me the topic connection details</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/topic_connect.png?raw=true" />
</details>

_Time to prepare some code to be run..._

### 2. Load the project into Gitpod

Development and running will be done within a Gitpod instance (more on that in a second).

#### 2a. Open Gitpod

To load the whole project (API + client) in your personal Gitpod workspace, please
Ctrl-click (or right-click and open in new tab) on the following button:

<a href="https://gitpod.io/#https://github.com/datastaxdevs/workshop-streaming-game"><img src="images/open_in_gitpod_button.svg" /></a>

(You may have to authenticate with Github or other providers along the process).
Then wait a couple of minutes for the installations to complete, at which point you
will see a message such as `CLIENT/API READY TO START` in the Gitpod console.

<details><summary>Show me what the Gitpod button does</summary>

- An IDE is started on a containerized machine image in the cloud
- there, this repo is cloned
- some initialization scripts are run (in particular, dependencies get installed)
- Gitpod offers a full IDE: you can work there, edit files, run commands in the console, use an internal browser, etc.

</details>

> In case you prefer to work _on your local computer_, no fear! You can simply keep
> a console open to run the React client (`cd client`) and another for the
> Python API (`cd api`). For the former
> you will have to `npm install` and for the latter (preferrably in a virtual environment
> to keep things tidy and clean) you will have to install the required dependencies
> e.g. with `pip install -r requirements.txt`.
> (Mac users will also have to do a `brew install libpulsar` for the API to work.)
> The rest of this readme will draw your
> attention to the occasional differences between the Gitpod and the local routes, but
> we'll generally assume that if you work locally you know what you are doing. Good luck!

#### 2b. Gitpod interface

This project is composed of two parts: client and API. For this reason, Gitpod
is configured to spawn _three_ different consoles: the "default" one for
general-purpose actions, an "api" console and a "client" console (these two
will start in the `api` and `client` subdirectories for you).
**You can switch between consoles by clicking on the items in the lower-right panels in your Gitpod**.

<details><summary>Show me a map of the Gitpod starting layout</summary>
1 = file explorer, 2 = editor, 3 = panel for console(s), 4 = console switcher.

<img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/gitpod_view.png?raw=true" />
</details>

> Note: for your convenience, you find this very README open within the Gitpod
> text editor.

### 3. API setup

There are a couple of things to do before you can launch the API:

#### 3a. Environment variables

You need to pass the connection URL and secret to the API for it to be able
to speak to the Streaming topic. To do so, first **go to the API console**
and make sure you are in the `api` subdirectory.

Then create a file `.env` by copying the `.env.sample` in the same directory,
with the commands

    cp .env.sample .env
    gp open .env

(the second line will simply open the `.env` file in the editor).
Fill the file with the values found earlier
on your Astra Streaming "Connect" tab (leave the other lines unchanged; _keep the quotes in the file_):

- `STREAMING_TENANT`: your very own tenant name as chosen earlier when creating the topic (step `1b`); it should be something like `gameserver-abc`.
- `SERVICE_URL`: it looks similar to `pulsar+ssl://pulsar-aws-useast2.streaming.datastax.com:6651`
- `ASTRA_TOKEN`: a very long string (about 500 random-looking chars), see step `1c`. You can copy it on the Astra UI without showing it.

> Note: treat your token as a personal secret: do not share it, do not commit it to the repo, store it in a safe place!

> Note: in case you gave a different namespace/name to your topic, update `.env` correspondingly.
> If, moreover, you work locally you may have to check the `TRUST_CERTS` variable as well, depending
> on your OS distribution. Look into the `.env` file for some suggestions.

#### 3b. Start the API

Make sure you are in the API console and in the `api` subdirectory.
You can now **start the API**:

    uvicorn api:app

You should see the API start and log some messages in the console, in particular

    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

Congratulations: the API is up and is ready to accept client requests.
Leave it running and turn your attention to the client.

> Note: this is how you start the API in a development environment. To deploy
> to production, you should set up a multi-process system service for `uvicorn`
> with the `--workers` option and put the whole thing behind a
> reverse proxy. _This is not covered here_.

### 4. Client setup

Make sure you **go to the client console** for the following
(to switch consoles, look at the lower-right panel in your Gitpod layout).
You should be in the `client` project subdirectory.

#### 4a. Install dependencies

First ensure all required dependencies are installed:

    npm install

> Note: the command would take a few minutes on a fresh directory; we secretly instructed Gitpod
> to preinstall them just to save you some time in this step - still, we want
> you to go through it. Obviously, if you are working on your local environment,
> this will be slower.

#### 4b. Start the client

The client is ready to go! **Launch it** in development mode with:

    npm start

Let's assume you are working within Gitpod, which wraps locally-exposed ports
and makes them accessible through ordinary HTTPS domain names.
As the client is available, Gitpod will automatically open it in its "simple browser",
using a domain such as `https://3000-tan-swallow-2yz174hp.ws-eu17.gitpod.io`.
This URL can be obtained also by typing, in the general-purpose Gitpod console,

    gp url 3000

(3000 being the port number locally used by npm to serve the client).
This will match the URL shown in the address bar of your simple browser.

Note that you can also take this URL and open the application in a new tab,
**which you are encouraged to do to use your full screen**.

> Note: we set up Gitpod for this workshop so as to make this URL accessible by anyone, to allow you
> to paste the link to your friends, thereby inviting them to your own game instance!

> If you are running everything locally on your computer, instead, you can
> open the client on `http://localhost:3000` and use the
> default API location of `ws://localhost:8000` to enter the game.

> Note: this is how you launch the client in development mode. For deploying
> to production, you should first build the project and then serve it from
> a static Web server. _This is not covered here_.

### 5. Play the game!

We finally have all pieces in place:

- an Astra Streaming topic;
- an API bridging it to ...
- ... a client ready to establish WebSocket connections.

It is time to play!

#### 5a. Enter the game

Change your name if you desire (a spider name is drawn at random for you).
You will also see that you are given a (read-only) unique player ID and that an API address
is configured for the client to establish WebSocket connections to.

> The API location points to the instance of the API running alongside the client:
> you should generally not have to change it (but please notice the protocol is
> either `ws` or `wss`, which stand for WebSocket and Secure WebSocket respectively).

To enter the game, click the "Enter Game" button.

<details><summary>Show me the "Enter Game" form</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/drapetisca_2.png?raw=true" />
</details>

Well done: you are in the game. You should see your player appear in the arena!

- To control your player, either use the on-screen arrow buttons or, after bringing the game field into focus, your keyboard's arrow keys;
- you can use the in-game chat box on the left.

<details><summary>Show me the player after entering the game</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/drapetisca_3.png?raw=true" />
</details>

Anything your player does is sent to the API through a WebSocket in the form of an "update message";
from there, it is published to the Astra Streaming topic. The API will then pick up the update
and broadcast to all players, whose client will process it, eventually leading to a refresh of the game status
on the front-end. All this happens in a near-real-time fashion at every action by every player.

> Note that the game shows the last sent message and the last received messages for you to better inspect
> the messaging pattern at play.

#### 5b. Try to cheat

Let's be honest: there's no multiplayer game without cheaters - at least, cheat attempts.
So, for example, try to _walk beyond the boundaries of the play area_, to see what happens.
Notice the "Position" caption on the left sidebar? If you keep an arrow key pressed
long enough, you will sure be able to bring that position to an illegal value such as `(-1, 0)`.
But as soon as you release the key, the position bounces back to a valid state.

Here's the trick: this "position", shown in the client, is nothing more than a variable
in the client's memory. Every update (including `(-1, 0)`) is sent to the API, which
is the sole actor in charge of validation: an illegal value will be corrected and sent back
to all clients. In particular, your own client will adjust knowledge of its own position
based on this feedback from the API - which is why you see the illegal value only briefly.

All of this must happen asynchronously, as is the nature of the communication between client
and API. There is a lesson here, which has been hard-earned by online game devs over the years:
_never leave validity checks in the hand of the client_.

> Remember the hordes of cheaters in ... er ... Diablo I ?

**Implications on the architecture**

Unfortunately such an all-server architecture is more complex to achieve.
One has to introduce a "generation counter" to avoid accidentally triggering
infinite loops of spurious player-position updates - you can see this
ever-increasing generation counter (`generation`) if you inspect the
player-position updates shown at the bottom of the application.

In the client code, the crucial bit is to accept updates to your-own-position
coming from the server, _only if they are recent enough_. For further inspection,
have a look at:

- API: usage of `validatePosition` at line 66 of `api.py`;
- Client: condition on `generation` at line 109 of `App.js` before invoking `setPlayerX` and `setPlayerY`.

> Note: in this architecture, we very much **want** to have a server between
> clients and Pulsar topic, with the responsibility of performing validations.
> Even more so in a complex game, where each client action (message) triggers
> potentially several actions in the world. But we want to mention, in passing by,
> that Pulsar also offers its own
> [native WebSocket interface](https://pulsar.apache.org/docs/en/client-libraries-websocket/)
> (and so does Astra Streaming),
> for clients to directly connect to topics using that protocol.

#### 5c. Bring your friends

But wait ... this is a _multiplayer_ game, isn't it? So, go ahead and open a new
browser tab, then enter the game as someone else.

Hooray! As soon as you move around with this new player,
you will see the whole architecture at work:

- client sends updates on your player's position through the "player websocket"
- API validates this update and publishes it to the Astra Streaming topic
- API receives new messages by listening to this same Astra Streaming topic
- API broadcasts updates on any player to all connected clients through the "world websocket"
- at each such update, the client's game arena is adjusted (for all connected clients)

What is really cool is that **you can give this URL to your friends** and have them
enter your very own game!

_Please do this and tell the world about how easy it is to build a multiplayer real-time
game with Astra Streaming!_

#### 5d. Fun with the Streaming UI

The Astra Streaming interface makes it possible to eavesdrop on the topic and
observe the messages passing through it. This may prove very useful for
debugging.

In the Astra Streaming UI, head to the "Try Me" tab and make sure the namespace
and the (producer, consumer) topics are set to the values used earlier. Also
ensure the connection is of type "Consume" before clicking "Connect".

<details><summary>Show me the "Try Me" interface</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/eavesdrop-marked.png?raw=true" />
</details>

You now have a privileged view over the messages flowing through the Streaming
topic. Now try writing something in the Chat box: can you see the corresponding
message in the Streaming UI?

What kind of message do you see, instead, if you move you player?

But wait, there's more: now you can **hack the system**! Indeed, this same interface lets you
produce surreptitious messages into the topic ("Send" button on the Streaming UI).
Try to insert a message such as:

    {
        "playerID": "nonexistent",
        "messageType": "chat",
        "payload": {
            "id": "000",
            "playerName": "Phantom Player",
            "text": "Booo!"
        }
    }

Or even something like

    {
        "playerID": "nonexistent",
        "messageType": "player",
        "payload": {
            "h": false,
            "x": 2,
            "y": 2,
            "generation": 0,
            "playerName": "Phantom Player"
        }
    }

What happens in the game UI when you to this?

Now, you just had a little fun: but this ability to manually intervene in the stream
of messages makes for a valuable debugging tool.

### 6. Homework instructions

Here are some more details on how to do the homework. We require two modifications
to the code, one on the API and one on the client. Once you change both, and restart,
you will be able to take a screenshot showing the new game appearance and submit
it to us!

#### 6a. Server side

We want a greeting message to be sent from the API to a new client right after
they join. To do so, the `api.py` already imports a function `makeWelcomeUpdate`
that returns a "chat message" ready to be sent through the WebSocket.

**You should add a line in the function `worldWSRoute` that creates the welcome
chat message and sends it to the WebSocket**. _Suggestion: this is really not
so different from the geometry update any new client receives upon connecting._

#### 6b. Client side

We want the player names on the game field to have the same color as the player
icons instead of always dark grey as they are now. If you look into `GameField.js`,
you'll notice that the SVG `text` element currently has a class name `"player-name"`.

**Make it so that players (self/other) use different class names in their `text`
element and have a color matching their icon**. _Suggestion: the right class name
is already calculated a few lines above for you to use (you can check in `App.css` as well)_.

#### 6c. Restart, test and take a screenshot

Remember to stop and restart the API: go to its console, hit Ctrl-C and
re-run `uvicorn api:app` to do so. All current WebSocket connections will
be lost.

The client is running in development mode, so it should pick up any changes
live and be immediately ready to serve the new version: reloading the app page
(and re-entering the game) should be enough.

At that point you will be playing the improved game: homework completed!

<details><summary>Show me the new features in the game</summary>
    <img src="https://github.com/datastaxdevs/workshop-streaming-game/raw/main/images/drapetisca_homework.png?raw=true" />
</details>

### 7. Selected topics

Let us briefly mention some specific parts of the implementation of this game.

#### 7a. WebSockets and React

API and client communicate through WebSockets: in this way, we have a connection
that is kept open for a long time and allows for a fast exchange of messages
without the overhead of establishing a new connection for each message;
moreover, this allows the server to push data without waiting for the client
to initiate the exchange (as in the obsolete technique of client-side polling).
WebSockets follow a robust and standardized [protocol](https://datatracker.ietf.org/doc/html/rfc6455)
which makes it possible for us developers to concentrate on our game logic
instead of having to worry about the communication internals.

In particular, this game uses two WebSockets, a "player" one for client-to-server
data transmission and a "world" one for server-to-client (i.e. game status updates).
You can find the corresponding variables `pws` and `wws` in the client code, respectively.

In Javascript, one _subscribes to an event_ on an open WebSocket, providing
a callback function with `webSocket.onmessage = <callback>`. But beware:
if you simply try to read a React state (such as `generation`) from within
the callback, you will generally get a stale value, _corresponding to the
state when the subscription was made_. In practice, the state variable
is "closed over". To overcome this problem, and be able to access the latest
updated value of the state, we declare a React "reference" with `useRef`
and, after linking it to the state we want to read, we use this reference
within the callback to dynamically retrieve the current value of the state.

Look at lines 42-43 and then 109 of `App.js`, for example.

#### 7b. FastAPI

This game's architecture involves a server. Indeed, we would not be able
to implement it using only serverless functions, at least not in a way similar
to what you see here, because of statefulness. We need a server able to sustain
the WebSocket connections for a long time, on one side, and to maintain
long-running subscriptions to the Pulsar topics on the other side.

We chose to create the API in Python, and to use
[FastAPI](https://fastapi.tiangolo.com/), for a couple of very valid
reasons. FastAPI integrates very well with the async/await features of modern
Python, which results in a more efficient handling of concurrency. Moreover,
it supports WebSockets (through its integration with
[Starlette](https://www.starlette.io/)) with a natural syntax that reduces
the need for boilerplate code to near zero.

> There are other cool features of FastAPI (besides its namesake high performance),
> which we do not employ here but make it a prime choice. There is a clever
> mechanism to handle route dependencies aimed at reducing the amount of "boring"
> code one has to write; and there is native support for those small tasks
> that sometimes you have to trigger asynchronously right after a request completes,
> those that in other frameworks would have required to set up machinery like Celery.

Have a look at `api.py` to see how a WebSocket connection is handled: decorating
a certain function with `@app.websocket(...)` is almost everything you need to
get started. One of the arguments of the function will represent the WebSocket
itself, supporting methods such as `send_text` and `receive_text`. Each
active WebSocket connection to the server will spawn an invocation of this
function, which will run as long as the connection is maintained: the support
for async/await guarantees that these concurrent executions of the
WebSocket function will be scheduled efficiently with no deadlocks.

#### 7c. SVG Tricks

One of the React components in the client code is the `GameField`, which
represents an area where we draw the players. This is a single large SVG
element, whose child elements are managed with the usual `jsx` syntax.

A technique that proved useful in this game is that of defining, and then
re-using multiple times, "patterns", basically as sprites. If you look
at the `GameField.js` render code, you notice that the SVG first declares
some `pattern` elements with certain `id`s (such as `lyco_other`).
These patterns are then employed in various parts of the SVG to "fill"
rectangles, which effectively makes it possible to use them as repeated sprites:

        <rect .... fill="url(#lyco_other)"></rect>

## The End

Congratulations, you made it to the end! Please share the URL of your game with
your friends: who does not love a little cozy spider gathering?

_(Please notice that after some inactivity your Gitpod instance will be hibernated:
you will need to re-start client and server to be able to play again.)_

Don't forget to complete and submit your [homework](#homework) to claim
your badge, and see you next time!

> DataStax Developers

![Theridion grallator](images/Theridion_grallator.png)
