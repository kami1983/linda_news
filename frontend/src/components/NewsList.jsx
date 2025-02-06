import React, { useState, useEffect } from 'react';
import { 
  Container, 
  List, 
  ListItem, 
  ListItemText,
  Typography,
  CircularProgress,
  Button,
  TextField,
  Box
} from '@mui/material';
import axios from 'axios';

const NewsList = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [aiAnalysis, setAiAnalysis] = useState({});
  const [analysisLoading, setAnalysisLoading] = useState({}); // 添加分析加载状态

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get('/api/news');
        setNews(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  const handleAiAnalysis = async (content, idx) => {
    try {
      setAnalysisLoading(prev => ({ ...prev, [idx]: true })); // 设置加载状态
      const res = await axios.post('/api/ai/news', { content });
      setAiAnalysis(prev => ({
        ...prev,
        [idx]: res.data.message
      }));
    } catch (error) {
      console.error('AI analysis failed:', error);
    } finally {
      setAnalysisLoading(prev => ({ ...prev, [idx]: false })); // 清除加载状态
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 4 }}>
        华尔街见闻 AI 分析
      </Typography>
      <List>
        {news.map((item, idx) => (
          <ListItem key={idx} sx={{ flexDirection: 'column', alignItems: 'flex-start', mb: 2 }}>
            <ListItemText
              primary={item[2]}
              secondary={
                <>
                  <Typography component="span" variant="body2" color="text.primary">
                    {item[0]}
                  </Typography>
                  <br />
                  <Typography component="span" variant="caption" color="text.secondary">
                    {item[1]}
                  </Typography>
                </>
              }
            />
            <Box sx={{ width: '100%', mt: 1 }}>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={() => handleAiAnalysis(item[0], idx)}
                disabled={analysisLoading[idx]}
                sx={{ mb: 1 }}
              >
                {analysisLoading[idx] ? (
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                    分析中...
                  </Box>
                ) : 'AI 分析'}
              </Button>
              {aiAnalysis[idx] && (
                <TextField
                  fullWidth
                  multiline
                  rows={15}
                  variant="outlined"
                  value={aiAnalysis[idx]}
                  InputProps={{
                    readOnly: true,
                  }}
                  sx={{ mt: 1 }}
                />
              )}
            </Box>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default NewsList; 