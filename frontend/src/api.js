import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// OCR endpoints
export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post('/ocr', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const getStatus = (jobId) => {
  return apiClient.get(`/status/${jobId}`)
}

export const getPreview = (jobId) => {
  return apiClient.get(`/preview/${jobId}`)
}

export const editText = (jobId, text) => {
  return apiClient.put(`/edit/${jobId}`, { text })
}

export const downloadFile = (jobId, format) => {
  return apiClient.get(`/download/${jobId}/${format}`, {
    responseType: 'blob'
  })
}

export const getOutputs = (jobId) => {
  return apiClient.get(`/outputs/${jobId}`)
}
