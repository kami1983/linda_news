import React, { useState, useEffect, useRef } from 'react';
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
  const [categoryLoading, setCategoryLoading] = useState({});
  const [conceptsLoading, setConceptsLoading] = useState({});
  const [categoryData, setCategoryData] = useState({});
  const [conceptsData, setConceptsData] = useState({});
  const [retryCount, setRetryCount] = useState(0);
  const [start, setStart] = useState(0);
  const size = 10; // 每次加载的条数
  const [loadingMore, setLoadingMore] = useState(false);

  // 最大重试次数
  const MAX_RETRIES = 3;

  // useEffect(() => {
  //   loadNews();
  // }, []);

  useEffect(() => {
    if (retryCount === 0) {
      loadNews();
    }
  }, [retryCount]);

  const resetRetryCount = () => {
    setRetryCount(0);
    loadNews();
  };

  const loadNews = async () => {
    setLoadingMore(true);
    try {
      if (retryCount < MAX_RETRIES) {
        const response = await axios.get(`/api/news?start=${start}&size=${size}`);
        const newNews = response.data;
        setNews(prevNews => [...prevNews, ...newNews]);
        setStart(prevStart => prevStart + size);

        // 使用 setTimeout 模拟延迟加载
        setTimeout(async () => {
          await Promise.all(newNews.map((item, idx) => {
            const globalIdx = start + idx; // 使用全局索引
            return handleCategoryAndConcepts(item[3], globalIdx);
          }));
        }, 1000); // 延迟 1 秒加载
      }
    } catch (error) {
      console.error('Error fetching news:', error);
      setRetryCount(prevCount => prevCount + 1);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

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

  const handleCategoryAndConcepts = async (news_id, idx) => {
    try {
      const res_category = await axios.post('/api/what_category', { news_id });
      setCategoryData(prev => ({
        ...prev,
        [idx]: res_category.data.message
      }));

      const res_concepts = await axios.post('/api/what_concepts', { news_id });
      setConceptsData(prev => ({
        ...prev,
        [idx]: res_concepts.data.message
      }));
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const observer = useRef();

  useEffect(() => {
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !loadingMore) {
        loadNews();
      }
    });

    const loadMoreRef = document.querySelector('#load-more');
    if (loadMoreRef) {
      observer.current.observe(loadMoreRef);
    }

    return () => {
      if (loadMoreRef) {
        observer.current.unobserve(loadMoreRef);
      }
    };
  }, [loadingMore]);

  // 计算时间差 
  // publishedTime=Tue, 18 Feb 2025 14:41:04 GMT
  const calculateTimeDifference = (publishedTime) => {
    const publishedDate = new Date(publishedTime);
    const currentDate = new Date();
    console.log('publishedTime:', publishedTime);
    console.log('publishedDate:', publishedDate);
    console.log('currentDate:', currentDate);

    // 将时间转换为 UTC 时间戳
    const timezoneOffset = 8 * 60 * 60 * 1000; // 8小时的毫秒数
    const publishedTimeUTC = publishedDate.getTime() ;
    const currentTimeUTC = currentDate.getTime() + timezoneOffset;

    const timeDifference = currentTimeUTC - publishedTimeUTC;
    const hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60));
    if (hoursDifference > 24) {
      return Math.floor(hoursDifference / 24) + '天'+ Math.floor(hoursDifference % 24) + '小时前';
    }
    return hoursDifference + '小时前';
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
      {retryCount >= MAX_RETRIES && (
        <Button onClick={resetRetryCount} variant="contained" color="primary">
          Retry fetch news
        </Button>
      )}
      <Grid container spacing={3}>
        {news.map((item, idx) => (
          <Grid item xs={12} sm={6} md={4} key={idx}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {item[2]} [{item[3]}]
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {calculateTimeDifference(item[2])}
                </Typography>
                <Typography variant="h6" color="text.primary">
                  {item[0]}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {categoryData[idx] ? categoryData[idx] : 'Loading category...'}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {conceptsData[idx] && Array.isArray(conceptsData[idx])
                    ? conceptsData[idx].join(', ')
                    : 'Loading concepts...'}
                </Typography>
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
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={() => handleCategoryAndConcepts(item[3], idx)}
                    disabled={categoryLoading[idx]}
                    sx={{ mb: 1 }}
                  >
                    {categoryLoading[idx] ? (
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                        分析中...
                      </Box>
                    ) : '刷新行业和概念分类'}
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
      <div id="load-more" style={{ height: '20px', margin: '10px 0', textAlign: 'center' }}>
        {loadingMore && <CircularProgress />}
      </div>
    </Container>
  );
};

export default NewsList; 