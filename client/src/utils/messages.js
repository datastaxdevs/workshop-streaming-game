// utility to serialize a standard player info message (name, position)
const packMessage = (generation, playerName, x, y, h) => {
  return JSON.stringify({
    generation,
    playerName,
    x,
    y,
    h
  })
}

export default packMessage
