import GameInputs from "./GameInputs"
import GameField from "./GameField"

const GameArea = ({playerName, playerID, playerMap, playerX, setPlayerX, playerY, setPlayerY, boardWidth, boardHeight}) => {

  return (<div>
    <GameInputs
      playerName={playerName}
      playerID={playerID}
      playerX={playerX}
      setPlayerX={setPlayerX}
      playerY={playerY}
      setPlayerY={setPlayerY}
    />
    <GameField
      playerMap={playerMap}
      playerID={playerID}
      boardWidth={boardWidth}
      boardHeight={boardHeight}
    />
  </div>)
}

export default GameArea;
