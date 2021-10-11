const settings = require('../settings')

const PlayerForm = ({playerName, setPlayerName, inGame, setInGame, setPlayerMap, playerID, setPlayerX, setPlayerY}) => {

  return (
    <div>
      <p>
        Your name:
        <input
          type="text"
          name="name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
        />
      </p>
      <p>
        Your ID:
        <input type="text" name="id" disabled="1" value={playerID} />
      </p>
      {!inGame && <button onClick={() => {
        setInGame(true)
        setPlayerMap({})
        setPlayerX(settings.HALF_SIZE_X - 1)
        setPlayerY(settings.HALF_SIZE_Y - 1)
      }}>
        Enter
      </button>}
      {inGame && <button onClick={() => setInGame(false)}>
        Leave
      </button>}
    </div>
  )

}

export default PlayerForm
