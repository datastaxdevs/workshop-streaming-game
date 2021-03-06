const PlayerForm = (props) => {

  const apiLocation = props.apiLocation
  const setApiLocation = props.setApiLocation
  const playerName = props.playerName
  const setPlayerName = props.setPlayerName
  const inGame = props.inGame
  const setInGame = props.setInGame
  const setPlayerInitialized = props.setPlayerInitialized
  const setPlayerMap = props.setPlayerMap
  const playerID = props.playerID
  const setLastSent = props.setLastSent
  const setLastReceived = props.setLastReceived
  const setGeneration = props.setGeneration

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
        setPlayerInitialized(false)
        setInGame(true)
        setPlayerMap({})
        setGeneration(0)
        setLastReceived(null)
        setLastSent(null)
      }}>
        Enter Game
      </button>
    </div>}
    {inGame && <div>
      <div className="game-title">
        <span className="game-title-name">Drapetisca</span>
        <span className="game-title-player-name">{playerName}</span>
        <button onClick={() => setInGame(false)}>
          Leave Game
        </button>
      </div>
    </div>}
  </div>)

}

export default PlayerForm
