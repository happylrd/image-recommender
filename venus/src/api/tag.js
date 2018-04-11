import axios from './http'

export function getTags (photoId) {
  const url = `/tags/photos/${photoId}`

  return axios.get(url)
    .then(res => {
      return Promise.resolve(res.data)
    })
}
