import React, { useState } from 'react';
import { Container, Typography, Button, Box, CircularProgress } from '@mui/material';
import axios from 'axios';

const UploadCsv = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('请选择一个CSV文件');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const response = await axios.post('/api/upload-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('文件上传失败');
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 4 }}>
        上传 CSV 文件
      </Typography>
      <Box sx={{ mb: 2 }}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={uploading}
      >
        {uploading ? (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
            上传中...
          </Box>
        ) : '上传'}
      </Button>
      {message && (
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
    </Container>
  );
};

export default UploadCsv; 