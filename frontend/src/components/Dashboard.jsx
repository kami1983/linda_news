import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Grid, Paper, List, ListItem, ListItemText, ListItemIcon, AppBar, Toolbar, IconButton } from '@mui/material';
import { Home as HomeIcon, Login as LoginIcon, Dashboard as DashboardIcon, Settings as SettingsIcon, UploadFile as UploadFileIcon } from '@mui/icons-material';
import axios from 'axios';
import Login from './Login';

import UploadCsv from './UploadCsv';


const Dashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedTab, setSelectedTab] = useState(0);

  useEffect(() => {
    // Check if the user is already logged in
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get('/api/current_user');
        if (response.data.status) {
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, []);
  
  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };


  return (
    <Container maxWidth="lg" sx={{ p: 0 }}>
      {!isAuthenticated ? (
        <Login onLogin={()=>handleLogin()} onLogout={()=>handleLogout()} />
      ) : (
        <>
          {/* <Typography variant="h4" sx={{ mb: 4, textAlign: 'center', color: 'primary.main' }}>
            Dashboard
          </Typography> */}
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={3}>
              <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
                <List component="nav">
                  <ListItem button selected={selectedTab === 0} onClick={() => setSelectedTab(0)}>
                    <ListItemIcon>
                      <LoginIcon color={selectedTab === 0 ? 'primary' : 'inherit'} />
                    </ListItemIcon>
                    <ListItemText primary="Logout" />
                  </ListItem>
                  <ListItem button selected={selectedTab === 1} onClick={() => setSelectedTab(1)}>
                    <ListItemIcon>
                      <UploadFileIcon color={selectedTab === 1 ? 'primary' : 'inherit'} />
                    </ListItemIcon>
                    <ListItemText primary="Upload CSV" />
                  </ListItem>
                  
                  {/* Add more menu items here as needed */}
                </List>
              </Paper>
            </Grid>
            <Grid item xs={9}>
              <Paper elevation={3} sx={{ p: 3 }}>
              {selectedTab === 0 && <Login onLogin={()=>handleLogin()} onLogout={()=>handleLogout()} />}
                {selectedTab === 1 && <UploadCsv />}
               
              </Paper>
            </Grid>
          </Grid>
        </>
      )}
    </Container>
  );
};

export default Dashboard; 