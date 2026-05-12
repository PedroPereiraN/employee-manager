import axios, { type ResponseType } from 'axios'

export interface Instance {
  baseURL: string
  headers: any
  responseType?: ResponseType
}

const API_BASE_URL = 'http://localhost:8000'

function appClientInstance({ baseURL, headers, responseType }: Instance) {
  const api = axios.create({
    baseURL: baseURL,
    responseType,
  })

  api.interceptors.request.use(
    (config) => {
      config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`

      const currentUserId = localStorage.getItem('d')
      const currentCompanyId = localStorage.getItem('cid')

      if (currentUserId) {
        config.headers['X-User-ID'] = currentUserId
      }

      if (currentCompanyId) {
        config.headers['X-Company-ID'] = currentCompanyId
      }

      if (headers.contentType && !(config.data instanceof FormData)) {
        config.headers['Content-Type'] = headers.contentType
      }

      if (headers.accept) {
        config.headers['accept'] = headers.accept
      }

      return config
    },

    (error) => {
      return Promise.reject(error)
    },
  )

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status == 401) {
        localStorage.removeItem('token')
        window.location.href = new URL('/', window.location.origin).toString()
      }

      return Promise.reject(error)
    },
  )

  return api
}

export const appClient = appClientInstance({
  baseURL: API_BASE_URL,
  headers: {
    contentType: 'application/json',
  },
})

export const formClient = appClientInstance({
  baseURL: API_BASE_URL,
  headers: {
    contentType: 'application/x-www-form-urlencoded',
  },
})
