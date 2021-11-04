<!--- STARTEXCLUDE --->
# Drapetisca: a multiplayer online game with Astra Streaming and Websockets

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/hemidactylus/drapetisca)
[![License Apache2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Discord](https://img.shields.io/discord/685554030159593522)](https://discord.com/widget?id=685554030159593522&theme=dark)

Time: *50 minutes*. Difficulty: *Intermediate*. [Start Building!](#lets-start)

A simple multiplayer online game featuring
* Astra Streaming (built on top of Apache Pulsar)
* WebSockets
* React.js for the front-ent
* the Python FastAPI framework for the back-end

<!--- ENDEXCLUDE --->

![Drapetisca screenshot](images/drapetisca_1.png)

## Objectives
* Understand the architecture of a streaming-based application
* Learn how Apache Pulsar works
* Learn about Websockets on client- and server-side
* Understand how a FastAPI server can bridge Pulsar topics and WebSockets
* Understand the structure of a Websocket React.js application
* **gain your very own online gaming platform to share with your friends!**

## Frequently asked questions

- *Can I run the workshop on my computer?*

> There is nothing preventing you from running the workshop on your own machine.
> If you do so, you will need
> * git installed on your local system
> * [node 15 and npm 7 or later](https://www.whitesourcesoftware.com/free-developer-tools/blog/update-node-js/)
> * Python v3.8+ installed on your local system
>
> In this readme, we try to provide instructions for local development as well - but keep in mind that
> the main focus is development on Gitpod, hence **We can't guarantee live support** about local development
> in order to keep on track with the schedule. However, we will do our best to give you the info you need to succeed.

- *What other prerequisites are there?*
> * You will need a github account
> * You will also need an Astra DB account: don't worry, we'll work through that in the following

- *Do I need to pay for anything for this workshop?*
> * **No.** All tools and services we provide here are FREE.

- *Will I get a certificate if I attend this workshop?*

> Attending the session is not enough. You need to complete the homeworks detailed below and you will get a nice badge.

- *Why "Drapetisca"?*

> _Drapetisca socialis_, known as "invisible spider", is a very small and hard-to-notice spider found throughout Europe.
> Since this is a multiplayer game that lets players have social interactions in the play area, why not choose a spider
> with "socialis" in its name?

## Materials for the Session

It doesn't matter if you join our workshop live or you prefer to do at your own pace, we have you covered. In this repository, you'll find everything you need for this workshop:

- [Slide deck](./slides/slides.pdf) TODO
- [Discord chat](https://bit.ly/cassandra-workshop)
- [Questions and Answers](https://community.datastax.com/)

## Homework

<img src="images/streaming-badge.png?raw=true" width="200" align="right" />

Don't forget to complete your upgrade and get your verified skill badge! Finish and submit your homework!

1. Complete the practice steps from this repository as described below.
2. TODO
3. TAKE A SCREENSHOT
5. Submit your homework [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) TODO

That's it, you are done! Expect an email in a few days!

# Let's start

## Table of contents

1. [Create your Astra Streaming instance](#1-login-or-register-to-astradb-and-create-database)
2. [Load the project into Gitpod](#2-)
3. [Set up the API](#3-)
4. [Set up the client](#4-)

3. [Create table **genre** with GraphQL](#3-create-table-genre-with-graphql)
4. [Insert data in **genre**  with GraphQL](#4-insert-data-in-the-table-with-graphql)
5. [Retrieve values of **genre** table](#5-retrieving-list-of-values)
6. [Create **movie** table](#6-creating-a-movies-table)
7. [Insert values in **movie** table](#7-insert-values-in-movie-table)
8. [Retrieve values from **movie** table](#8-retrieve-values-from-movie-tables)
9. [Load a CSV DataSet](#9-load-a-csv-dataset)

## Astra setup

### 1. Create your Astra Streaming instance

_**`Astra Streaming`** is the simplest way to get a streaming infrastructure based on Apache Pulsar
with zero operations at all - just push the button and get your streaming.
No credit card required - with the free tier comes a generous monthly-renewed credit for you to use._

_**`Astra Streaming`** is tightly integrated with `Astra DB`, the database-as-a-service
used in most of our other workshops. **If you already have an Astra DB account, you can use that
one in the following!**_

For more information on Astra Streaming, look at [the docs](https://docs.datastax.com/en/astra-streaming/docs/).
For more information on Apache Pulsar, here is [the documentation](https://pulsar.apache.org/docs/en/concepts-overview/).

#### 1a. Register

Register and sign in to Astra at `https://astra.datastax.com` by clicking this button:

<a href="https://astra.dev/11-17"><img src="images/create_astra_button.png" /></a>

_you can use your `Github`, `Google` accounts or register with an `email`.
Choose a password with minimum 8 characters, containing upper and lowercase letters, at least one number and special character.
You may be asked to verify your email, so make sure you have access to it._

<details><summary>Show me the steps</summary>
    <img src="https://github.com/hemidactylus/drapetisca/raw/main/images/astra_signup.gif?raw=true" />
</details>

#### 1b. Create streaming

Once registered and logged in, you will be able to create a streaming for use in this workshop.

> Heads up! Astra lets you also create Databases in the cloud (based on Apache Cassandra); in this workshop we will not need to,
> but keep that in mind. You can also effortlessly connect your streaming topics and an Astra DB instance to enrich your app!

Now it's time to create a new Astra Streaming topic, that will convey all messages for this app.

- Go to your Astra console, locate the "Create Streaming" button on the left and click on it.
- Set up a new Tenant (remember Pulsar has a multi-tenant architecture): _you have to find a globally unique name for it_,
so for instance if `gameserver` is already taken by someone, try `gameserver0`, `gameserver-abc` or something similar.
Pick the provider-region you like and finally hit "Create Tenant". **Remember the name of your tenant for the API setup step later**.
- You'll shortly see the dashboard for your newly-created Tenant. Go to the "Topics" tab to create a new one (we will stay in the "default" namespace).
- In the "Topics" tab, click "Add Topic" and name it `worldupdates` (persistent = yes, partitioned = no). Click "Save" to confirm topic creation.

> Note: technically you can name your namespace and topic anything you want - but then you have to make sure
> the environment settings for your API code are changed accordingly (see later).

<details><summary>Show me the steps</summary>
    <img src="https://github.com/hemidactylus/drapetisca/raw/main/images/astra_create_streaming_topic.gif?raw=true" />
</details>

#### 1c. Check connection details

While you are at it, have a look at the information needed to connect to the topic
from the API code. While still in the tenant dashboard, find the "Connect" tab and click on it: you will see a listing of "Tenant Details".
You will later need the "Broker Service URL" and the "Token" values (the latter is hidden but can be copied nevertheless).

<details><summary>Show me the topic connection details</summary>
    <img src="https://github.com/hemidactylus/drapetisca/raw/main/images/topic_connect.png?raw=true" />
</details>

Congratulations! Your topic is being created, which takes less than one minute, and is now ready to receive and
dispatch the stream of messages that will make your game work!
_Time to prepare some code to be run..._


### 2. Load the project into Gitpod

Development and running will be done within a Gitpod instance (more on that in a second).

#### 2a. Open Gitpod

To load the whole project (API + client) in your personal Gitpod workspace, please
Ctrl-click (or right-click and open in new tab) on the following button:

<a href="https://gitpod.io/#https://github.com/hemidactylus/drapetisca"><img src="images/open_in_gitpod_button.svg" /></a>

(You may have to authenticate with Github or other providers along the process).
Then wait a couple of minutes for the installations to complete, at which point you
will see a message such as `CLIENT/API READY TO START` in the Gitpod console.

<details><summary>Show me what the Gitpod button does</summary>

- An IDE is started on a virtual machine in the cloud
- this repo is cloned there
- some initialization scripts are run (in particular, dependencies get installed)
- Gitpod offers a full IDE: you can work there, edit files, run commands in the console, use an internal browser, etc.

</details>

> In case you prefer to work _on your local computer_, no fear! You can simply keep
> a console open to run the React client (`cd client`) and another for the
> Python API (`cd api`). For the former
> you will have to `npm install` and for the latter (preferrably in a virtual environment
> to keep things tidy and clean) you will have to install the required dependencies
> e.g. with `pip install -r requirements.txt`. The rest of this readme will draw your
> attention to the occasional differences between the Gitpod and the local routes, but
> we'll generally assume that if you work locally you know what you are doing. Good luck!

#### 2b. Gitpod interface

Gitpod works as an in-browser IDE: 

This project is composed of two parts: client and API. For this reason, Gitpod
is configured to spawn _three_ different consoles: the "default" one for
general-purpose actions, an "api" console and a "client" console (these two
will start in the `api` and `client` subdirectories for you).
**You can switch between consoles by clicking on the items in the lower-right panels in your Gitpod**.

<details><summary>Show me a map of the Gitpod starting layout</summary>
    <img src="https://github.com/hemidactylus/drapetisca/raw/main/images/gitpod_view.png?raw=true" />
    1 = file explorer, 2 = editor, 3 = panel for console(s), 4 = console switcher.
</details>

> Note: for your convenience, you find this very README open within the Gitpod
> text editor.

### 3. API setup

There are a couple of things to do before you can launch the API:

#### 3a. Environment variables

You need to pass the connection URL and secret to the API for it to be able
to speak to the Streaming topic. To do so, first **go to the API console**.

Then create a file `.env` by copying the `.env.sample` in the same directory,
with the commands

    cp ../.env.sample ../.env
    gp open ../.env

(the second will simply open the `.env` file in the editor)
and filling it with the values found earlier
on your Astra Streaming "Connect" tab (leave the other lines unchanged):

- `TENANT_NAME`: your very own tenant name as chosen earlier when creating the topic (step `1b`).
- `SERVICE_URL`: it looks similar to `pulsar+ssl://pulsar-aws-useast2.streaming.datastax.com:6651`
- `ASTRA_TOKEN`: a very long string (about 500 random-looking chars), see step `1c`. You can copy it without showing it.

> Note: treat your token as a personal secret: do not share it, do not commit it to the repo, store it in a safe place!

Make sure you are in the API shell. Export these environment variables for the API to pick them up when it starts:

    . ../.env

> Note: in case you gave a different namespace/name to your topic, update `.env` correspondingly.
> If, moreover, you work locally with a CentOS distribution you may have to check the `TRUST_CERTS` variable as well:
> check the "Connect" tab on your Astra Streaming console, looking for the Python/Consumer code sample there.

#### 3b. Settings file

=========================
=========================
=========================
=========================
=========================





### API shell


_Explanations on how the API works..._

Launch the API with:

    uvicorn api:app --reload

you will see the API start, happily ready to accept requests. Leave it running and let's turn to the client.

### Client shell

Switch to the client shell. We took care of preinstalling all required dependencies for you;
nevertheless, let us ensure all required dependencies are there:

    npm install

Now you simply have to start the client, which will open in the "simple browser" within Gitpod:

    npm start

> If you are running everything locally on your computer, you would be able
> to open the client on `http://localhost:3000` at this point and use the
> default API location of `ws://localhost:8000` to enter the game.

However, we are working within Gitpod, which wraps locally-exposed ports
and makes them potentially accessible over the Internet.
Have a look at the address bar
in Gitpod's simple browser: it has been automatically converted from the
above `localhost` address to something such as
`https://3000-tan-swallow-2yz174hp.ws-eu17.gitpod.io`.

_Explanations on how the client works ..._

### Play the game!

We have a client and an API ready to accept (Websocket) connections:
it is time to play!

The client lets you customize your player name and gives you a unique player ID.

It also needs the address to reach the API. Now, if you are running locally you
would find the API at `ws://localhost:8000`, but since
we are working within Gitpod it is necessary to modify
the "API Location" to reflect the Gitpod-provided domain.

Fortunately, the client does that for you and the field is pre-filled
with a Websocket address corresponding to the API running in your Gitpod
instance.

> To obtain the above, in any case, you can either run the command
> `gp url 8000 | sed s/https/wss/` and copy
> the output or simply take the client address as in the example above and replace
> `3000` with `8000` (the API listen on port 8000), and `https` with `wss`
> (we are using the secure Websocket protocol). Your API Location will look
> something like `wss://8000-tan-swallow-2yz174hp.ws-eu17.gitpod.io`.

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

But this is a _multiplayer_ game, isn't it? So Let us open a new
browser tab and enter the same client URL as above (the one on port 3000).
Enter a different player name and the same API Location you built above, then
hit "Enter Game". Hooray! As soon as you move around with this new player,
you will see the whole architecture at work:

- client sends updates on your player's position through the "player websocket"
- API validates this update and writes it to the Astra Streaming topic
- API receives new messages by listening to this same Astra Streaming topic
- API broadcasts updates on any player to all connected clients through the "world websocket"
- at each such update, the client's game arena is adjusted

What is really cool is that **you can give this URL to your friends** and have them
enter your very own multiplayer game!

_Please do this and tell the world about how easy it is to build a multiplayer real-time
game with Astra Streaming!_

## Fun with the Streaming UI

The Astra Streaming interface makes it possible to eavesdrop on the topic and
observe the messages passing through it. This may prove very useful for
debugging.

In the Astra Streaming UI, head to the "Try Me" tab and make sure the namespace
and the (producer, consumer) topics are set to the values used earlier. Also
ensure the connection is of type "Consume" before clicking "Connect".

![astra-ui-topic-connection](images/eavesdrop-marked.png)

Now, if you move your player around in the client app, you will see the
corresponding messages flowing through the Streaming topic.

Of course now we want to "hack the system"! Indeed this same interface lets
you produce messages into the topic: let us insert a message such as

    {"playerName": "INTRUDER", "playerID": "1n7rud3r", "y": 3, "x": 3}

and check what happens on the game arena!

## Finally

_Let me give you all MY address and let us run like crazy around my arena!_

_"Now form a circle shape! Now a smiley..."_
