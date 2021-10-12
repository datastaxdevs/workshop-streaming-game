import './App.css';

import { useEffect, useState } from "react"

import PlayerForm from "./components/PlayerForm"
import GameArea from "./components/GameArea"


import packMessage from "./utils/messages"
import replaceValue from "./utils/replaceValue"

const settings = require('./settings')
const uuid = require('uuid');
const playerID = uuid.v4();

// web-sockets
let wws = null;
let pws = null;

const App = () => {

  const [playerName, setPlayerName] = useState('player');
  const [apiLocation, setApiLocation] = useState(settings.DEFAULT_API_LOCATION);
  const [inGame, setInGame] = useState(false);
  const [playerMap, setPlayerMap] = useState({});
  const [playerX, setPlayerX] = useState(settings.HALF_SIZE_X-1)
  const [playerY, setPlayerY] = useState(settings.HALF_SIZE_Y-1)

  // keyboard-controlled movements
  const handleKeyDown = ev => {
    if(inGame){
      if ( ev.keyCode === 37 ){
        setPlayerX( x => x-1 )
      }
      if ( ev.keyCode === 38 ){
        setPlayerY( y => y-1 )
      }
      if ( ev.keyCode === 39 ){
        setPlayerX( x => x+1 )
      }
      if ( ev.keyCode === 40 ){
        setPlayerY( y => y+1 )
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
          pws.send(packMessage(playerName, playerX, playerY))
        }

        wws.onmessage = evt => {
          const thatPlayerUpdate = JSON.parse(evt.data)
          // Received update on some player through the 'world' websocket
          const thatPlayerID = thatPlayerUpdate.playerID
          setPlayerMap(plMap => {
            const newPlMap = replaceValue(plMap, thatPlayerID, thatPlayerUpdate)
            return newPlMap
          })
        }
      }

    }else{
      if(wws !== null || pws !== null){
        // it is time to disconnect the websockets

        if(pws && pws.readyState === 1){
          pws.send(packMessage('', null, null))
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
        pws.send(packMessage(playerName, playerX, playerY))
      }
  
    }
  }, [inGame, playerName, playerX, playerY])

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
      />}
    </div>
  );
}

export default App;
