const GameField = ({playerMap, brickList, foodMap, playerID, boardWidth, boardHeight}) => {

  return (
    <svg className="game-field" width="100%" height="700" preserveAspectRatio="none" viewBox={`0 0 ${100 * boardWidth} ${100 * boardHeight}`}>
      <defs>
       <pattern id="lyco_other" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="lyco_other.svg"></image>
       </pattern>
       <pattern id="lyco_self" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="lyco_self.svg"></image>
       </pattern>
       <pattern id="hearts" x="65" y="40" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="20" y="10" width="60" height="60" href="hearts.svg"></image>
       </pattern>
       <pattern id="brick" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="brick.svg"></image>
       </pattern>
       <pattern id="food" x="50" y="50" width="100" height="100" patternUnits="userSpaceOnUse">
         <image x="0" y="0" width="100" height="100" href="food.svg"></image>
       </pattern>
      </defs>
      <rect width={100 * boardWidth} height={100 * boardHeight} style={{fill: '#f9ffbb'}} />
      { brickList.map( (brickInfo) => {
        return (<g key={brickInfo.name} transform={`translate(${brickInfo.x * 100},${brickInfo.y * 100})`}>
          <g transform='translate(50,50)'>
            <rect x="-50" y="-50" height="100" width="100" fill={`url(#brick)`}></rect>
          </g>
        </g>)
      })}
      { Object.entries(foodMap).map( ([foodID, foodInfo]) => {
        return (<g key={foodID} transform={`translate(${foodInfo.x * 100},${foodInfo.y * 100})`}>
          <g transform='translate(50,50)'>
            <rect x="-50" y="-50" height="100" width="100" fill={`url(#food)`}></rect>
            {foodInfo.h && <rect x="-50" y="-50" width="100" height="100" fill='url(#hearts)'></rect>}
          </g>
        </g>)
      })}

      { Object.entries(playerMap).map( ([thatPlayerID, thatPlayerInfo]) => {
        const patternName = thatPlayerID === playerID ? 'lyco_self' : 'lyco_other'
        const playerClassName = thatPlayerID === playerID ? 'player-self' : 'player-other'
        return (<g key={thatPlayerID} transform={`translate(${thatPlayerInfo.x * 100},${thatPlayerInfo.y * 100})`}>
          <g transform='translate(50,50)'>
            <rect x="-50" y="-50" height="100" width="100" fill={`url(#${patternName})`}></rect>
            {thatPlayerInfo.h && <rect x="-50" y="-50" width="100" height="100" fill='url(#hearts)'></rect>}
            <g transform={`translate(0,${thatPlayerInfo.y + 1 >= boardHeight? -70 : 70})`}>
              <text className="player-name" textAnchor='middle' fontSize='40'>
                {thatPlayerInfo.name}
              </text>
            </g>
          </g>
        </g>)
      })}
    </svg>
  )
}

export default GameField;
