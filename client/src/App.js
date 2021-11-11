import './App.css';

import { useEffect, useState, useRef } from "react"

import PlayerForm from "./components/PlayerForm"
import GameArea from "./components/GameArea"

import {packPlayerMessage, packChatMessage} from "./utils/messages"
import replaceValue from "./utils/replaceValue"
import guessAPILocation from "./utils/guessAPILocation"
import getRandomSpiderName from "./utils/names"

const settings = require('./settings')
const uuid = require('uuid');
const playerID = uuid.v4();

// web-sockets
let wws = null;
let pws = null;

const App = () => {

  const proposedAPILocation = guessAPILocation(window.location.href, settings.DEFAULT_API_LOCATION);

  const [playerName, setPlayerName] = useState(getRandomSpiderName());
  const [apiLocation, setApiLocation] = useState(proposedAPILocation);
  const [inGame, setInGame] = useState(false);
  const [playerMap, setPlayerMap] = useState({});
  const [playerX, setPlayerX] = useState(null);
  const [playerY, setPlayerY] = useState(null);
  const [halfSizeX, setHalfSizeX] = useState(null);
  const [halfSizeY, setHalfSizeY] = useState(null);
  const [playerH, setPlayerH] = useState(false)
  const [generation, setGeneration] = useState(0)
  const [lastSent, setLastSent] = useState(null)
  const [lastReceived, setLastReceived] = useState(null)
  const [chatItems, setChatItems] = useState([])

  // With useRef we can make the updated state accessible from within the callback
  // that we will attach to the websocket.
  // see https://stackoverflow.com/questions/57847594/react-hooks-accessing-up-to-date-state-from-within-a-callback
  const generationRef = useRef()
  generationRef.current = generation
  // Same for the player position/status, since it will be accessed within callbacks:
  const playerXRef = useRef()
  playerXRef.current = playerX
  const playerYRef = useRef()
  playerYRef.current = playerY
  const playerHRef = useRef()
  playerHRef.current = playerH

  // keyboard-controlled movements
  const handleKeyDown = ev => {
    if(inGame){
      if ( ev.keyCode === 37 ){
        setPlayerX( x => x-1 )
        setPlayerH(false)
      }
      if ( ev.keyCode === 38 ){
        setPlayerY( y => y-1 )
        setPlayerH(false)
      }
      if ( ev.keyCode === 39 ){
        setPlayerX( x => x+1 )
        setPlayerH(false)
      }
      if ( ev.keyCode === 40 ){
        setPlayerY( y => y+1 )
        setPlayerH(false)
      }
      if( ev.keyCode === 72 ){
        setPlayerH(h => !h)
      }
    }
  }

  useEffect( () => {
    if(inGame){

      if(wws === null || pws === null){
        // we must create the websockets and attach callbacks to them

        wws = new WebSocket(`${apiLocation}/ws/world/${playerID}`)
        pws = new WebSocket(`${apiLocation}/ws/player/${playerID}`)

        pws.onopen = evt => {
          const msg = packPlayerMessage(generationRef.current, playerName, playerXRef.current, playerYRef.current, playerHRef.current)
          setLastSent(msg)
          pws.send(msg)
        }

        wws.onmessage = evt => {
          setLastReceived(evt.data)

          try {

            const updateMsg = JSON.parse(evt.data)

            if ( updateMsg.messageType === 'player' ){

              // Received update on some player through the 'world' websocket
              const thatPlayerID = updateMsg.playerID
              setPlayerMap(plMap => {
                const newPlMap = replaceValue(plMap, thatPlayerID, updateMsg.payload)
                return newPlMap
              })
              // We compare generations before receiving an update to self, to avoid update loops
              // from player updates delivered back to us asynchronously:
              if ((thatPlayerID === playerID) && (updateMsg.payload.generation >= generationRef.current - 1)){
                if ( updateMsg.payload.x !== null){
                  setPlayerX(updateMsg.payload.x)
                  setPlayerY(updateMsg.payload.y)
                }
              }
            } else if ( updateMsg.messageType === 'geometry' ) {
              // we received initial geometry info from the API
              setHalfSizeX(updateMsg.payload.halfSizeX)
              setHalfSizeY(updateMsg.payload.halfSizeY)
              setPlayerX(updateMsg.payload.halfSizeX - 1)
              setPlayerY(updateMsg.payload.halfSizeY - 1)
              setPlayerH(false)
            } else if ( updateMsg.messageType === 'chat' ) {
              // we received a new chat item. Let's make room for it
              // first we add the playerID to the chat-item object
              const chatPayload = {...updateMsg.payload, ...{playerID: updateMsg.playerID}}
              // then we concatenate it to the items to display (discarding the oldest if necessary)
              setChatItems( items => items.concat([chatPayload]).slice(-settings.MAX_ITEMS_IN_CHAT) )
            } else {
              // another messageType
              console.log(`Ignoring messageType = ${updateMsg.messageType} ... for now`)
            }

          } catch (e) {
            console.log(`Error "${e}" while receiving message "${evt.data}". Ignoring message, the show must go on`)
          }

        }
      }

    } else {
      if(wws !== null || pws !== null){

        // we notify the API that we are leaving
        if(pws && pws.readyState === 1){
          const msg = packPlayerMessage(generationRef.current, playerName, null, null, playerH)
          setLastSent(msg)
          pws.send(msg)
        }
        setGeneration( g => g+1 )

        // it is time to disconnect the websockets
        if(wws === null){
          wws.disconnect()
          wws = null;
        }
        if(pws === null){
          pws.disconnect()
          pws = null;
        }
      }
    }
  // eslint-disable-next-line
  }, [inGame])

  const sendChatItem = text => {
    const ttext = text.trim()
    if (ttext !== '' && pws && pws.readyState === 1){
      const msg = packChatMessage(playerName, text)
      setLastSent(msg)
      pws.send(msg)
    }
  }

  useEffect( () => {
    if (inGame) {

      if(pws && pws.readyState === 1){
        const msg = packPlayerMessage(generationRef.current, playerName, playerX, playerY, playerH)
        setLastSent(msg)
        pws.send(msg)
      }

      // we increment the generation number to recognize and ignore 'stale' player updates bouncing back to us
      setGeneration( g => g+1 )
  
    }
  // we are handling generation increase explicitly within this hook, so we don't react to it:
  // eslint-disable-next-line
  }, [inGame, playerName, playerX, playerY, playerH])

  return (
    <div className="App">
      <header className="App-header">
        <PlayerForm
          apiLocation={apiLocation}
          setApiLocation={setApiLocation}
          playerName={playerName}
          setPlayerName={setPlayerName}
          inGame ={inGame}
          setInGame ={setInGame}
          setPlayerMap={setPlayerMap}
          playerID={playerID}
          setLastSent={setLastSent}
          setLastReceived={setLastReceived}
          setGeneration={setGeneration}
        />
      </header>
      {inGame && <GameArea
        playerName={playerName}
        playerID={playerID}
        playerMap={playerMap}
        playerX={playerX}
        setPlayerX={setPlayerX}
        playerY={playerY}
        setPlayerY={setPlayerY}
        boardWidth={2 * halfSizeX - 1}
        boardHeight={2 * halfSizeY - 1}
        handleKeyDown={handleKeyDown}
        lastSent={lastSent}
        lastReceived={lastReceived}
        setGeneration={setGeneration}
        setPlayerH={setPlayerH}
        halfSizeX={halfSizeX}
        halfSizeY={halfSizeY}
        chatItems={chatItems}
        sendChatItem={sendChatItem}
      />}
    </div>
  );
}

export default App;
