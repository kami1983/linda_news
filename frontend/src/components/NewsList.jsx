import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
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
  const [analysisLoading, setAnalysisLoading] = useState({});
  const [importanceLoading, setImportanceLoading] = useState({});
  

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
      setAnalysisLoading(prev => ({ ...prev, [idx]: true }));
      const res = await axios.post('/api/ai/news', { content });
      setAiAnalysis(prev => ({
        ...prev,
        [idx]: res.data.message
      }));
    } catch (error) {
      console.error('AI analysis failed:', error);
    } finally {
      setAnalysisLoading(prev => ({ ...prev, [idx]: false }));
    }
  };

  const handleAiImportance = async (content, idx) => {
    try {
      setImportanceLoading(prev => ({ ...prev, [idx]: true }));
      const res = await axios.post('/api/ai/importance', { content });
      setAiAnalysis(prev => ({
        ...prev,
        [idx]: res.data.message
      }));
    } catch (error) {
      console.error('AI importance analysis failed:', error);
    } finally {
      setImportanceLoading(prev => ({ ...prev, [idx]: false }));
    }
  };

  const handleCategoryAndConcepts = async (content, idx) => {
    try {
      // 调用 /api/what_category 接口
      const res_category = await axios.post('/api/what_category', { content });
      setCategoryData(prev => ({
        ...prev,
        [idx]: res_category.data.message
      }));

      // 调用 /api/what_concepts 接口
      const res_concepts = await axios.post('/api/what_concepts', { content });
      setConceptsData(prev => ({
        ...prev,
        [idx]: res_concepts.data.message
      }));
      
    } catch (error) {
      console.error('Error fetching data:', error);
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
        投资分析参考
      </Typography>
      <Grid container spacing={3}>
        {news.map((item, idx) => (
          <Grid item xs={12} sm={6} md={4} key={idx}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {item[2]}
                </Typography>
                <Typography variant="h6" color="text.primary">
                  {item[0]}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Category
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Concepts 1, Concepts 2, Concepts 3
                </Typography>
                {/* <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                  {item[1]}
                </Typography> */}
                <Box sx={{ mt: 2 }}>
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
                  &nbsp;&nbsp;&nbsp;&nbsp;
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={() => handleAiImportance(item[0], idx)}
                    disabled={importanceLoading[idx]}
                    sx={{ mb: 1 }}
                  >
                    {importanceLoading[idx] ? (
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                        分析中...
                      </Box>
                    ) : 'AI 重要性分析'}
                  </Button>
                </Box>
                {aiAnalysis[idx] && (
                  <TextField
                    fullWidth
                    multiline
                    rows={20}
                    variant="outlined"
                    value={aiAnalysis[idx]}
                    InputProps={{
                      readOnly: true,
                    }}
                    sx={{ mt: 1 }}
                  />
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
    </Container>
  );
};

export default NewsList; 