// utility to upsert a new key-value pair into an object
export const updatePositionMapValue = (origMap, repKey, newValue) => {
  const newObj = origMap
  newObj[repKey] = newValue
  // we take out players with null x or y values. This happens in the transient case
  // of the onboarding of a player, when setting x and y occurs sequentially:
  // for a brief moment one is set and the other is still null).
  // Doing this saves some headache in the rendering code.
  return Object.fromEntries(Object.entries(newObj).filter( ([k,v]) => v.x !== null && v.y !== null))
}

export const removePlayerMapEntry = (origMap, delKey) => {
    return Object.fromEntries(Object.entries(origMap).filter( ([k,v]) => k !== delKey))
}
