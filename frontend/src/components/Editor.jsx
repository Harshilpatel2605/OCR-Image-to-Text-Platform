import React, { useState, useEffect } from 'react'
import { getPreview, editText, downloadFile, getOutputs } from '../api'

export default function Editor({ jobId, onBack }) {
  const [text, setText] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState(null)
  const [outputs, setOutputs] = useState(null)

  useEffect(() => {
    const loadPreview = async () => {
      try {
        const response = await getPreview(jobId)
        setText(response.data.text)
        
        // Also fetch outputs
        const outputsResponse = await getOutputs(jobId)
        setOutputs(outputsResponse.data.outputs)
        
        setIsLoading(false)
      } catch (error) {
        if (error.response?.status === 202) {
          // Still processing
          setTimeout(loadPreview, 2000)
        } else {
          setError('Failed to load preview')
          setIsLoading(false)
        }
      }
    }

    loadPreview()
  }, [jobId])

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await editText(jobId, text)
      
      // Refresh outputs
      const outputsResponse = await getOutputs(jobId)
      setOutputs(outputsResponse.data.outputs)
      
      alert('Changes saved successfully!')
      setIsSaving(false)
    } catch (error) {
      alert('Failed to save: ' + error.message)
      setIsSaving(false)
    }
  }

  const handleDownload = async (format) => {
    try {
      const response = await downloadFile(jobId, format)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `document.${format}`)
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
    } catch (error) {
      alert('Download failed: ' + error.message)
    }
  }

  if (isLoading) {
    return (
      <div className="card">
        <div className="loading-text">
          <div className="spinner"></div>
          <span>Processing your file...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="status error">{error}</div>
        <button className="btn" onClick={onBack}>Back to Upload</button>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Edit Extracted Text</h2>
      <div className="editor-wrapper" style={{ marginTop: '20px' }}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Your extracted text will appear here..."
        />
      </div>

      <div className="btn-group">
        <button
          className="btn"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
        <button className="btn btn-secondary" onClick={onBack}>
          Back
        </button>
      </div>

      {outputs && (
        <div className="download-links">
          <h3 style={{ marginTop: '20px', marginBottom: '10px' }}>Download Options</h3>
          <button
            className="btn btn-small"
            onClick={() => handleDownload('txt')}
          >
            Download as TXT
          </button>
          <button
            className="btn btn-small"
            onClick={() => handleDownload('docx')}
          >
            Download as DOCX
          </button>
          <button
            className="btn btn-small"
            onClick={() => handleDownload('pdf')}
          >
            Download as PDF
          </button>
        </div>
      )}
    </div>
  )
}
