"use client"

import React, { useState } from 'react';
import { Upload, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

interface UploadStatus {
  type: 'success' | 'error';
  message: string;
  data?: {
    [key: string]: {
      originalName: string;
      size: number;
      hash: string;
    };
  };
}

const FileUpload = () => {
  const [files, setFiles] = useState<{
    markdown: File | null;
    csv: File | null;
  }>({
    markdown: null,
    csv: null
  });
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, fileType: string) => {
    if (!e.target.files) return;
    const file = e.target.files[0];
    setFiles(prev => ({
      ...prev,
      [fileType]: file
    }));
    setUploadStatus(null);
  };

  const handleUpload = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    if (!files.markdown || !files.csv) {
      setUploadStatus({
        type: 'error',
        message: 'Please select both Markdown and CSV files'
      });
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('markdown', files.markdown);
    formData.append('csv', files.csv);

    const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://email-automation-backend-cyan.vercel.app'; // Use correct API URL

    try {
      console.log("API URL: ", API_URL); // Debugging the API URL
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      setUploadStatus({
        type: 'success',
        message: 'Files uploaded successfully!',
        data: data.files
      });

      // Clear file selections
      setFiles({ markdown: null, csv: null });

    } catch (error) {
      console.error('Upload failed', error); // Log the error for debugging
      setUploadStatus({
        type: 'error',
        message: (error as Error).message
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6 border">
        <h2 className="text-2xl font-semibold mb-4">File Upload</h2>

        <form onSubmit={handleUpload} className="space-y-4">
          {/* Markdown File Input */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Markdown File
            </label>
            <input
              type="file"
              accept=".md,.markdown"
              onChange={(e) => handleFileChange(e, 'markdown')}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            {files.markdown && (
              <p className="mt-1 text-sm text-gray-500">
                Selected: {files.markdown.name}
              </p>
            )}
          </div>

          {/* CSV File Input */}
          <div>
            <label className="block text-sm font-medium mb-2">
              CSV File
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => handleFileChange(e, 'csv')}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            {files.csv && (
              <p className="mt-1 text-sm text-gray-500">
                Selected: {files.csv.name}
              </p>
            )}
          </div>

          {/* Upload Button */}
          <button
            type="submit"
            disabled={uploading || !files.markdown || !files.csv}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
          >
            <Upload size={20} />
            {uploading ? 'Uploading...' : 'Upload Files'}
          </button>
        </form>

        {/* Status Messages */}
        {uploadStatus && (
          <Alert className={`mt-4 ${
            uploadStatus.type === 'success' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
          }`}>
            {uploadStatus.type === 'success' ? (
              <CheckCircle2 className="h-4 w-4 text-green-600" />
            ) : (
              <AlertCircle className="h-4 w-4 text-red-600" />
            )}
            <AlertTitle className={
              uploadStatus.type === 'success' ? 'text-green-800' : 'text-red-800'
            }>
              {uploadStatus.type === 'success' ? 'Success' : 'Error'}
            </AlertTitle>
            <AlertDescription className={
              uploadStatus.type === 'success' ? 'text-green-700' : 'text-red-700'
            }>
              {uploadStatus.message}
            </AlertDescription>
          </Alert>
        )}

        {/* File Details After Success */}
        {uploadStatus?.type === 'success' && uploadStatus.data && (
          <div className="mt-4 p-4 bg-gray-50 rounded-md">
            <h3 className="font-medium mb-2">Uploaded Files:</h3>
            <div className="space-y-2 text-sm">
              {Object.entries(uploadStatus.data).map(([type, info]) => (
                <div key={type} className="border-b pb-2">
                  <p className="font-medium capitalize">{type} File:</p>
                  <p>Original name: {info.originalName}</p>
                  <p>Size: {(info.size / 1024).toFixed(2)} KB</p>
                  <p className="truncate">Hash: {info.hash}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
