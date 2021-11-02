// we try to build the API location from the client's URL
// (in a rather crude manner)
const guessAPILocation = (clientURL, defaultURL) => {
  if ((clientURL.indexOf('3000') >= 0) && (clientURL.indexOf('http') >= 0)){

    // this cleanup is to make the guess work within Gitpod, where the "(mini-)browser" reports an URL
    // such as "wss://8000-apricot-lizard-sa8u19n5.ws-eu17.gitpod.io/?vscodeBrowserReqId=1635860969945"
    // (as opposed to "ordinary" browsers where the URL would end with "...gitpod.io/")
    const gpCleanedClientURL = clientURL.indexOf('?') >= 0 ? clientURL.slice(0, clientURL.indexOf('?')) : clientURL

    // now the 'standard' guesswork can start
    const apiLoc = gpCleanedClientURL.replace('3000', '8000').replace('http', 'ws')
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
