import GameInputs from "./GameInputs"
import GameField from "./GameField"

const GameArea = ({playerName, playerID, playerMap, playerX, setPlayerX, playerY, setPlayerY, boardWidth, boardHeight, handleKeyDown}) => {

  return (
    <div class="container" onKeyDown={handleKeyDown} tabindex="0">
      <div class="sidebar">
        <GameInputs
          playerName={playerName}
          playerID={playerID}
          playerX={playerX}
          setPlayerX={setPlayerX}
          playerY={playerY}
          setPlayerY={setPlayerY}
        />
      </div>
      <div class="content">
        <GameField
          playerMap={playerMap}
          playerID={playerID}
          boardWidth={boardWidth}
          boardHeight={boardHeight}
        />
      </div>
    </div>
  );

}

export default GameArea;
