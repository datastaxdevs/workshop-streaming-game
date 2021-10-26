// utility to serialize a standard player info message (name, position, ...)
const packPlayerMessage = (generation, playerName, x, y, h) => {
  return JSON.stringify({
    messageType: 'player',
    payload: {
      generation,
      playerName,
      x,
      y,
      h
    }
  })
}

export default packPlayerMessage
