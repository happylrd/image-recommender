import axios from './http'

export function login (username, password) {
  const url = '/users/login'

  return axios.post(url, {
    username: username,
    password: password
  })
    .then(res => {
      return Promise.resolve(res.headers.authorization)
      // return Promise.resolve(res.data)
    })
}

export function getInfo (username, token) {
  const url = `/users/${username}`

  return axios.get(url, {
    headers: {
      'Authorization': `${token}`
    }
  })
    .then(res => {
      return Promise.resolve(res.data)
    })
}

export function getRecPhotos (userId, token) {
  const url = `/users/rec/${userId}`

  return axios.get(url, {
    headers: {
      'Authorization': `${token}`
    }
  })
    .then(res => {
      return Promise.resolve(res.data)
    })
}
