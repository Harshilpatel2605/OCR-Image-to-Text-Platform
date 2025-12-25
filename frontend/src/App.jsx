import React, { useState } from 'react'
import Upload from './components/Upload'
import Editor from './components/Editor'

export default function App() {
  const [jobId, setJobId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleReset = () => {
    setJobId(null)
    setIsLoading(false)
  }

  return (
    <div className="container">
      <header className="header">
        <h1>OCR Image-to-Text Platform</h1>
        <p>Convert scanned documents and images to editable text</p>
      </header>

      <div className="main-content">
        {!jobId ? (
          <div className="card" style={{ gridColumn: '1 / -1' }}>
            <h2>Upload Your Document</h2>
            <Upload
              onFileSelected={setJobId}
              onLoading={setIsLoading}
            />
            {isLoading && (
              <div className="loading-text" style={{ marginTop: '20px' }}>
                <div className="spinner"></div>
                <span>Uploading and processing...</span>
              </div>
            )}
          </div>
        ) : (
          <>
            <div className="card" style={{ gridColumn: '1 / -1' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <p style={{ color: '#666', fontSize: '14px', marginBottom: '5px' }}>Job ID</p>
                  <p style={{ fontFamily: 'monospace', fontSize: '12px', color: '#999' }}>
                    {jobId}
                  </p>
                </div>
                <button className="btn btn-secondary" onClick={handleReset}>
                  Start Over
                </button>
              </div>
            </div>
            <Editor jobId={jobId} onBack={handleReset} />
          </>
        )}
      </div>
    </div>
  )
}
