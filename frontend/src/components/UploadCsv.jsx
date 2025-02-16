import React, { useState } from 'react';
import { Container, Typography, Button, Select, MenuItem, FormControl, InputLabel, Box } from '@mui/material';
import axios from 'axios';

const UploadCsv = () => {
  const [file, setFile] = useState(null);
  const [type, setType] = useState(1); // 默认类型为1

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTypeChange = (event) => {
    setType(event.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('请选择一个文件');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    try {
      const response = await axios.post('/api/upload_csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('文件上传成功');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('文件上传失败');
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" sx={{ my: 4, textAlign: 'center' }}>
        上传 CSV 文件
      </Typography>
      <Box sx={{ mb: 2 }}>
        <FormControl fullWidth>
          <InputLabel id="type-select-label">文件类型</InputLabel>
          <Select
            labelId="type-select-label"
            value={type}
            label="文件类型"
            onChange={handleTypeChange}
          >
            <MenuItem value={1}>概念数据 CSV</MenuItem>
            <MenuItem value={2}>行业数据 CSV</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="upload-file-input"
        />
        <label htmlFor="upload-file-input">
          <Button variant="contained" component="span">
            选择文件
          </Button>
        </label>
        {file && (
          <Typography variant="body1" sx={{ ml: 2 }}>
            {file.name}
          </Typography>
        )}
      </Box>
      <Button variant="contained" color="primary" onClick={handleUpload} fullWidth>
        上传
      </Button>
    </Container>
  );
};

export default UploadCsv; 