import React, { useState } from 'react';
import { Container, Typography, Button, Select, MenuItem, FormControl, InputLabel, Box, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import axios from 'axios';

const UploadCsv = () => {
  const [file, setFile] = useState(null);
  const [type, setType] = useState(1); // 默认类型为1
  const [open, setOpen] = useState(false); // 控制对话框的打开状态

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

  const handleClickOpen = () => {
    if (!file) {
      alert('请选择一个文件');
      return;
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirmUpload = () => {
    handleUpload();
    setOpen(false);
  };

  const handleRebuildCsvHeads = async () => {
    try {
      // Fetch the current label
      const labelResponse = await axios.get('/api/get_csv_label');
      const currentLabel = parseInt(labelResponse.data.message);

      // Increment the label
      const newLabel = currentLabel + 1;

      // Call the rebuild endpoint with the new label
      const response = await axios.get(`/api/rebuild_csv_heads?label=${newLabel}`);

      alert(`文件版本更新成功: ${newLabel}`);
    } catch (error) {
      console.error('Error updating file version:', error);
      alert('文件版本更新失败');
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" sx={{ my: 4, textAlign: 'center' }}>
        上传知识库 CSV 文件
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
            <MenuItem value={1}>行业数据 CSV</MenuItem>
            <MenuItem value={2}>概念数据 CSV</MenuItem>
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
      <Button variant="contained" color="primary" onClick={handleClickOpen} fullWidth sx={{ mb: 2 }}>
        上传
      </Button>
      <Button variant="outlined" color="secondary" onClick={handleRebuildCsvHeads} fullWidth>
        更新文件版本
      </Button>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>确认上传</DialogTitle>
        <DialogContent>
          <DialogContentText>
            您即将上传以下文件：
            <br />
            文件名称: {file ? file.name : ''}
            <br />
            文件类型: {type === 1 ? '行业数据 CSV' : '概念数据 CSV'}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="secondary">
            取消
          </Button>
          <Button onClick={handleConfirmUpload} color="primary">
            确认
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default UploadCsv; 