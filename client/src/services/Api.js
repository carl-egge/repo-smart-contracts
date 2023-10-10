import axios from 'axios'

export default() => {
  return axios.create({
    baseURL: 'http://'+location.hostname+':8081'   // <- for production
    // baseURL: 'http://'+location.hostname+':8000'     // <- for development
  })
}
