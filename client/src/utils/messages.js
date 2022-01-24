const uuid = require('uuid');

// utility to serialize a standard player info message (name, position, ...)
export const packPlayerMessage = (x, y, h, generation, name) => {
  return JSON.stringify({
    messageType: 'player',
    payload: {
      generation,
      name,
      x,
      y,
      h
    }
  })
}

// utility to serialize a player chat entry
export const packChatMessage = (name, text) => {
  return JSON.stringify({
    messageType: 'chat',
    payload: {
      name,
      text,
      id: uuid.v4(),
    }
  })
}

export const packEnteringMessage = (name) => {
  return JSON.stringify({
    messageType: 'entering',
    payload: {
      name,
    }
  })
}

export const packLeavingMessage = (name) => {
  return JSON.stringify({
    messageType: 'leaving',
    payload: {
      name,
    }
  })
}