// src/components/KnowledgeBase.jsx
import React, { useState } from 'react';
import { Container, Typography, Box, Grid, Paper, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import { DateRange as DateRangeIcon } from '@mui/icons-material';
import ValuationHistory from './ValuationHistory';

const KnowledgeBase = () => {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" sx={{ mb: 4, textAlign: 'center', color: 'primary.main' }}>
        Knowledge Base
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={3}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <List component="nav">
              <ListItem button selected={selectedTab === 0} onClick={() => setSelectedTab(0)}>
                <ListItemIcon>
                  <DateRangeIcon color={selectedTab === 0 ? 'primary' : 'inherit'} />
                </ListItemIcon>
                <ListItemText primary="Valuation History" />
              </ListItem>

              {/* Add more menu items here as needed */}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={9}>
          <Paper elevation={3} sx={{ p: 3 }}>
            {selectedTab === 0 && <ValuationHistory />}
            {/* Render other components based on the selected tab */}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default KnowledgeBase;