// src/components/KnowledgeBase.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Box, Paper, List, ListItem, ListItemText } from '@mui/material';

const KnowledgeBase = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" sx={{ mb: 4, textAlign: 'center', color: 'primary.main' }}>
          Knowledge Base
        </Typography>
        <Box sx={{ my: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Menu
          </Typography>
          <List>
            <ListItem button component={Link} to="/upload">
              <ListItemText primary="Upload CSV" />
            </ListItem>
            {/* Add more menu items here as needed */}
          </List>
        </Box>
      </Paper>
    </Container>
  );
};

export default KnowledgeBase;