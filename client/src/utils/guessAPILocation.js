// we try to build the API location from the client's URL
// (in a rather crude manner)
const guessAPILocation = (clientURL, defaultURL) => {
  if ((clientURL.indexOf('3000') >= 0) && (clientURL.indexOf('http') >= 0)){
    const apiLoc = clientURL.replace('3000', '8000').replace('http', 'ws')
    if (apiLoc[apiLoc.length - 1] === '/'){
      // get rid of trailing '/'
      return apiLoc.slice(0, -1)
    }else{
      return apiLoc
    }
  }else{
    return defaultURL
  }
}

export default guessAPILocation
