const GameInputs = ({playerName, playerID, playerX, setPlayerX, playerY, setPlayerY}) => {

  return (<div>
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
      <div style={{'grid-column': 'span 3', 'font-size': '75%'}}>({playerX}, {playerY})</div>
    </div>
  </div>)
}

export default GameInputs;

