import GameInputs from "./GameInputs"
import GameField from "./GameField"

const GameArea = (props) => {

  const playerName = props.playerName
  const playerID = props.playerID
  const playerMap = props.playerMap
  const playerX = props.playerX
  const setPlayerX = props.setPlayerX
  const playerY = props.playerY
  const setPlayerY = props.setPlayerY
  const boardWidth = props.boardWidth
  const boardHeight = props.boardHeight
  const handleKeyDown = props.handleKeyDown
  const lastSent = props.lastSent
  const lastReceived = props.lastReceived
  const setPlayerH = props.setPlayerH
  const chatItems = props.chatItems
  const sendChatItem = props.sendChatItem

  return (
    <div>
      <div className="container">
        <div className="sidebar">
          <GameInputs
            playerName={playerName}
            playerID={playerID}
            playerX={playerX}
            setPlayerX={setPlayerX}
            playerY={playerY}
            setPlayerY={setPlayerY}
            setPlayerH={setPlayerH}
            chatItems={chatItems}
            sendChatItem={sendChatItem}
            boardWidth={boardWidth}
            boardHeight={boardHeight}
          />
        </div>
        <div className="content" onKeyDown={handleKeyDown} tabIndex="0">
          <GameField
            playerMap={playerMap}
            playerID={playerID}
            boardWidth={boardWidth}
            boardHeight={boardHeight}
          />
        </div>
      </div>
      <div className="statusbar">
        <p>Last sent: <code className="game-message">
          {lastSent}
        </code></p>
        <p>Last received: <code className="game-message">
          {lastReceived}
        </code></p>
      </div>
    </div>
  );

}

export default GameArea;
