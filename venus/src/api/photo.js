import axios from './http'

export function getHotPhotos () {
  const url = '/photos'

  return axios.get(url)
    .then(res => {
      return Promise.resolve(res.data)
    })
}

export function getPhoto (photoId) {
  const url = `/photos/${photoId}`

  return axios.get(url)
    .then(res => {
      return Promise.resolve(res.data)
    })
}

export function getRecPhotos (photoId) {
  const url = `/photos/rec/${photoId}`

  return axios.get(url)
    .then(res => {
      return Promise.resolve(res.data)
    })
}

export function getPhotosByTag (tagName) {
  const url = `/photos/tags/${tagName}`

  return axios.get(url)
    .then(res => {
      return Promise.resolve(res.data)
    })
}
