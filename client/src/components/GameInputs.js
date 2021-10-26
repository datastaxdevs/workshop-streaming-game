const GameInputs = ({playerName, playerID, playerX, setPlayerX, playerY, setPlayerY, setPlayerH}) => {

  return (<div>
    <div>At ({playerX}, {playerY})</div>
    <div className="grid-container">
      <div></div>
      <div>
        <button onClick={ () => {setPlayerY( y => y-1 ); setPlayerH(false)} }> &uArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => {setPlayerX( x => x-1 ); setPlayerH(false)} }> &lArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => {setPlayerX( x => x+1 ); setPlayerH(false)} }> &rArr; </button>
      </div>
      <div></div>
      <div>
        <button onClick={ () => {setPlayerY( y => y+1 ); setPlayerH(false)} }> &dArr; </button>
      </div>
      <div></div>
    </div>
    <div className="astra-logo">
      Powered by
    </div>
    <div>
      <a className="astra-logo" href="https://astra.datastax.com/" target="_blank" rel="noreferrer">
        <img src="astra-streaming-stacked-pos.png" alt="Astra Streaming" />
      </a>
    </div>
  </div>)
}

export default GameInputs;

