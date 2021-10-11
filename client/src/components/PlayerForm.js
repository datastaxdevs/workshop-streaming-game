const settings = require('../settings')

const PlayerForm = ({apiLocation, setApiLocation, playerName, setPlayerName, inGame, setInGame, setPlayerMap, playerID, setPlayerX, setPlayerY}) => {

  return (<div>
    {!inGame && <div>
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
      <p>
        API Location:
        <input
          type="text"
          name="apilocation"
          value={apiLocation}
          onChange={(e) => setApiLocation(e.target.value)}
        />
      </p>
      <button onClick={() => {
        setInGame(true)
        setPlayerMap({})
        setPlayerX(settings.HALF_SIZE_X - 1)
        setPlayerY(settings.HALF_SIZE_Y - 1)
      }}>
        Enter Game
      </button>
    </div>}
    {inGame && <div>
      <button onClick={() => setInGame(false)}>
        Leave Game
      </button>
    </div>}
  </div>)

}

export default PlayerForm
