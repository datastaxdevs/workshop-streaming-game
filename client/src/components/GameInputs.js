const GameInputs = ({playerName, playerID, playerX, setPlayerX, playerY, setPlayerY}) => {

  return (<div>
    <div>At ({playerX}, {playerY})</div>
    <div className="grid-container">
      <div></div>
      <div>
        <button onClick={ () => setPlayerY( y => y-1 ) }> &uArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => setPlayerX( x => x-1 ) }> &lArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => setPlayerX( x => x+1 ) }> &rArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => setPlayerY( y => y+1 ) }> &dArr; </button>
      </div>
      <div></div>
    </div>
    <div className="astra-logo">
      Powered by
    </div>
    <div>
      <a className="astra-logo" href="https://astra.datastax.com/" target="_blank" rel="noreferrer">
        <img src="astra-streaming-stacked-pos.png" />
      </a>
    </div>
  </div>)
}

export default GameInputs;

