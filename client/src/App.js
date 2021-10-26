import './App.css';

import { useEffect, useState, useRef } from "react"

import PlayerForm from "./components/PlayerForm"
import GameArea from "./components/GameArea"


import packMessage from "./utils/messages"
import replaceValue from "./utils/replaceValue"
import guessAPILocation from "./utils/guessAPILocation"

const settings = require('./settings')
const uuid = require('uuid');
const playerID = uuid.v4();

// web-sockets
let wws = null;
let pws = null;

const App = () => {

  const proposedAPILocation = guessAPILocation(window.location.href, settings.DEFAULT_API_LOCATION);

  const [playerName, setPlayerName] = useState('player');
  const [apiLocation, setApiLocation] = useState(proposedAPILocation);
  const [inGame, setInGame] = useState(false);
  const [playerMap, setPlayerMap] = useState({});
  const [playerX, setPlayerX] = useState(settings.HALF_SIZE_X-1)
  const [playerY, setPlayerY] = useState(settings.HALF_SIZE_Y-1)
  const [playerH, setPlayerH] = useState(false)
  const [generation, setGeneration] = useState(0)
  const [lastSent, setLastSent] = useState(null)
  const [lastReceived, setLastReceived] = useState(null)

  // With useRef we can make the updated state accessible from within the callback
  // that we will attach to the websocket.
  // see https://stackoverflow.com/questions/57847594/react-hooks-accessing-up-to-date-state-from-within-a-callback
  const generationRef = useRef()
  generationRef.current = generation

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
          const msg = packMessage(generationRef.current, playerName, playerX, playerY, playerH)
          setLastSent(msg)
          pws.send(msg)
        }

        wws.onmessage = evt => {
          setLastReceived(evt.data)
          const thatPlayerUpdate = JSON.parse(evt.data)
          // Received update on some player through the 'world' websocket
          const thatPlayerID = thatPlayerUpdate.playerID
          setPlayerMap(plMap => {
            const newPlMap = replaceValue(plMap, thatPlayerID, thatPlayerUpdate)
            return newPlMap
          })
          // We compare generations before receiving an update to self, to avoid update loops
          // from player updates delivered back to us asynchronously:
          if ((thatPlayerID === playerID) && (thatPlayerUpdate.generation >= generationRef.current - 1)){
            setPlayerX(thatPlayerUpdate.x)
            setPlayerY(thatPlayerUpdate.y)
          }
        }
      }

    }else{
      if(wws !== null || pws !== null){
        // it is time to disconnect the websockets

        if(pws && pws.readyState === 1){
          const msg = packMessage(generationRef.current, '', null, null, false)
          setLastSent(msg)
          pws.send(msg)
        }

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

  useEffect( () => {
    if (inGame) {

      if(pws && pws.readyState === 1){
        const msg = packMessage(generationRef.current, playerName, playerX, playerY, playerH)
        setLastSent(msg)
        pws.send(msg)
      }

      setGeneration( g => g+1 )
  
    }
  // we are handle generation increase in this hook:
  // eslint-disable-next-line
  }, [inGame, playerName, playerX, playerY, playerH])

  useEffect(() => {

    document.addEventListener('keydown', handleKeyDown);

    return function cleanup() {
      document.removeEventListener('keydown', handleKeyDown);
    }
  // eslint-disable-next-line
  }, []);

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
          setPlayerX={setPlayerX}
          setPlayerY={setPlayerY}
          setLastSent={setLastSent}
          setLastReceived={setLastReceived}
          setGeneration={setGeneration}
          setPlayerH={setPlayerH}
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
        boardWidth={2 * settings.HALF_SIZE_X - 1}
        boardHeight={2 * settings.HALF_SIZE_Y - 1}
        handleKeyDown={handleKeyDown}
        lastSent={lastSent}
        lastReceived={lastReceived}
        setGeneration={setGeneration}
        setPlayerH={setPlayerH}
      />}
    </div>
  );
}

export default App;
