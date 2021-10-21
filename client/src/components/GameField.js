const GameField = ({playerMap, playerID, boardWidth, boardHeight}) => {

  return (
    <svg width="600" height="450" viewBox={`0 0 ${100 * boardWidth} ${100 * boardHeight}`}>
      <defs>
       <pattern id="lyco_other" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="lyco_other.svg"></image>
       </pattern>
       <pattern id="lyco_self" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="lyco_self.svg"></image>
       </pattern>
      </defs>
      <rect width={100 * boardWidth} height={100 * boardHeight} style={{fill: '#f9ffbb'}} />
      { Object.entries(playerMap).map( ([thatPlayerID, thatPlayerInfo]) => {
        const patternName = thatPlayerID === playerID ? 'lyco_self' : 'lyco_other'
        return (<g key={thatPlayerID} transform={`translate(${thatPlayerInfo.x * 100},${thatPlayerInfo.y * 100})`}>
          <g transform='translate(50,50)'>
            <circle cx="0" cy="0" r="50" fill={`url(#${patternName})`}></circle>
            <g transform='translate(0,50)'>
              <text textAnchor='middle' fill='#404040' fontSize='40'>{thatPlayerInfo.playerName}</text>
            </g>
          </g>
        </g>)
      })}
    </svg>
  )
}

export default GameField;
