import './App.css';

import { useEffect, useState } from "react"

import PlayerForm from "./components/PlayerForm"
import GameArea from "./components/GameArea"


import packMessage from "./utils/messages"
import replaceValue from "./utils/replaceValue"

const settings = require('./settings')
const uuid = require('uuid');
const playerID = uuid.v4();

const wws = new WebSocket(`ws://localhost:8000/ws/world/${playerID}`)
const pws = new WebSocket(`ws://localhost:8000/ws/player/${playerID}`)

const App = () => {

  const [playerName, setPlayerName] = useState('player');
  const [inGame, setInGame] = useState(false);
  const [playerMap, setPlayerMap] = useState({});
  const [playerX, setPlayerX] = useState(settings.HALF_SIZE_X-1)
  const [playerY, setPlayerY] = useState(settings.HALF_SIZE_Y-1)

  useEffect( () => {
    if (inGame) {
      // Entering game

      if(pws.readyState === 1){
        pws.send(packMessage(playerName, playerX, playerY))
      }

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
  
    } else {
      // Leaving game

      wws.onmessage = evt => {}
      pws.onopen = evt => {}

      if(pws.readyState === 1){
        pws.send(packMessage(playerName, null, null))
      }

    }
  }, [inGame, playerName, playerX, playerY])

  return (
    <div className="App">
      <header className="App-header">
        <PlayerForm
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
      />}
    </div>
  );
}

export default App;
