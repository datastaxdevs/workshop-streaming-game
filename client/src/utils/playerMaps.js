// utility to upsert a new key-value pair into an object
export const updatePlayerMapValue = (origMap, repKey, newValue) => {
  // newValue.payload.x and newValue.payload.y should never be null here
  if (newValue.x === null || newValue.y === null){
    console.log('Received a nully coord update, huh?', repKey, JSON.stringify(newValue))
  }
  //
  const newObj = origMap
  newObj[repKey] = newValue
  return Object.fromEntries(Object.entries(newObj).filter( ([k,v]) => v.x !== null && v.y !== null))
}

export const removePlayerMapEntry = (origMap, delKey) => {
    return Object.fromEntries(Object.entries(origMap).filter( ([k,v]) => k !== delKey))
}
