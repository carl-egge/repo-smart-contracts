import axios from 'axios'

export default() => {
  return axios.create({
    baseURL: '/api' //'http://'+location.hostname+':5000/api'   // <- for production
    // baseURL: 'http://'+location.hostname+':8000/api'     // <- for development
  })
}
