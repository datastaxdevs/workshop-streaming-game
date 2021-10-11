const GameField = ({playerMap, playerID, boardWidth, boardHeight}) => {

  return (
    <svg width="400" height="300" viewBox={`0 0 ${100 * boardWidth} ${100 * boardHeight}`}>\
      <rect width={100 * boardWidth} height={100 * boardHeight} style={{fill: '#f3ffab'}} />
      { Object.entries(playerMap).map( ([thatPlayerID, thatPlayerInfo]) => {
        const plColor = thatPlayerID === playerID ? '#b0b0f0' : '#b0f0b0'
        return (<g key={thatPlayerID} transform={`translate(${thatPlayerInfo.x * 100},${thatPlayerInfo.y * 100})`}>
          <circle cx="50" cy="50" r="40" fill={plColor} />
          <g transform='translate(50,50)'>
            <text textAnchor='middle' fill='#404040' fontSize='40'>{thatPlayerInfo.playerName}</text>
          </g>
        </g>)
      })}
    </svg>
  )
}

export default GameField;
