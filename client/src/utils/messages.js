// utility to serialize a standard player info message (name, position)
const packMessage = (generation, playerName, x, y) => {
  return JSON.stringify({
    generation,
    playerName,
    x,
    y
  })
}

export default packMessage
