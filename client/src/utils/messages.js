// utility to serialize a standard player info message (name, position)
const packMessage = (playerName, x, y) => {
  return JSON.stringify({
    playerName,
    x,
    y
  })
}

export default packMessage
