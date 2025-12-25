import React, { useState } from 'react'
import { uploadFile } from '../api'

export default function Upload({ onFileSelected, onLoading }) {
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = React.useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFile = async (file) => {
    if (!file) return

    const allowed = ['image/jpeg', 'image/png', 'image/bmp', 'application/pdf']
    if (!allowed.includes(file.type)) {
      alert('Please upload an image (JPG, PNG, BMP) or PDF')
      return
    }

    onLoading(true)
    try {
      const response = await uploadFile(file)
      onFileSelected(response.data.job_id)
    } catch (error) {
      alert('Upload failed: ' + error.message)
      onLoading(false)
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  return (
    <div
      className={`upload-area ${dragActive ? 'dragover' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".jpg,.jpeg,.png,.bmp,.pdf"
        onChange={handleChange}
      />
      <div>
        <p style={{ fontSize: '24px', marginBottom: '10px' }}>📁</p>
        <p>
          <strong>Click to upload or drag and drop</strong>
        </p>
        <p>PNG, JPG, BMP or PDF</p>
      </div>
    </div>
  )
}
