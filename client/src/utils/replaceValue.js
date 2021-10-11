// utility to upsert a new key-value pair into an object
// and to clean those entries with null x or y (representing players who left)
const replaceValue = (origMap, repKey, newValue) => {
  const newObj = origMap
  newObj[repKey] = newValue
  return Object.fromEntries(Object.entries(newObj).filter( ([k,v]) => v.x !== null && v.y !== null))
}

export default replaceValue
