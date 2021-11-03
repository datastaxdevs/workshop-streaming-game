const uuid = require('uuid');

// utility to serialize a standard player info message (name, position, ...)
export const packPlayerMessage = (generation, playerName, x, y, h) => {
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

// utility to serialize a player chat entry
export const packChatMessage = (playerName, text) => {
  return JSON.stringify({
    messageType: 'chat',
    payload: {
      playerName,
      text,
      id: uuid.v4(),
    }
  })
}
