import React, { useState } from 'react';
import { Container, Typography, Box, Grid, Paper, List, ListItem, ListItemText, ListItemIcon, AppBar, Toolbar, IconButton } from '@mui/material';
import { Home as HomeIcon, Dashboard as DashboardIcon, Settings as SettingsIcon } from '@mui/icons-material';
import Login from './Login';

const Dashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  return (
    <Container maxWidth="lg" sx={{ p: 0 }}>
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                Dashboard
              </Typography>
              <IconButton color="inherit">
                <SettingsIcon />
              </IconButton>
            </Toolbar>
          </AppBar>
          <Grid container spacing={3} sx={{ mt: 0 }}>
            <Grid item xs={3}>
              <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
                <List component="nav">
                  <ListItem button>
                    <ListItemIcon>
                      <HomeIcon />
                    </ListItemIcon>
                    <ListItemText primary="Home" />
                  </ListItem>
                  <ListItem button>
                    <ListItemIcon>
                      <DashboardIcon />
                    </ListItemIcon>
                    <ListItemText primary="Dashboard" />
                  </ListItem>
                  {/* Add more menu items here as needed */}
                </List>
              </Paper>
            </Grid>
            <Grid item xs={9}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h5" sx={{ mb: 2 }}>
                  Welcome to the Dashboard
                </Typography>
                <Box sx={{ mb: 2 }}>
                  {/* Add charts, tables, or other content here */}
                  <Typography variant="body1">
                    Here you can find insights and analytics about your data.
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </>
      )}
    </Container>
  );
};

export default Dashboard; 