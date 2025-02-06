import React, { useState, useEffect } from 'react';
import { 
  Container, 
  List, 
  ListItem, 
  ListItemText,
  Typography,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const NewsList = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get('/api/ai/news');
        setNews(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

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
        {news.map((item) => (
          <ListItem key={item.id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <ListItemText
              primary={item.title}
              secondary={
                <>
                  <Typography component="span" variant="body2" color="text.primary">
                    {item.content}
                  </Typography>
                  <br />
                  <Typography component="span" variant="caption" color="text.secondary">
                    {new Date(item.publish_time).toLocaleString()}
                  </Typography>
                </>
              }
            />
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default NewsList; 