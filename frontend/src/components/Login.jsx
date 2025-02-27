import React, { useState, useEffect } from 'react';
import { TextField, Button, Typography, Container, Box, Paper } from '@mui/material';
import axios from 'axios';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  root: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  },
  paper: {
    padding: '20px',
    maxWidth: '400px',
    width: '100%',
    textAlign: 'center',
  },
  title: {
    marginBottom: '20px',
  },
  button: {
    marginTop: '20px',
  },
});

const Login = ({ onLogin, onLogout }) => {
  const classes = useStyles();
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    // 检查用户是否已登录
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get('/api/current_user');
        if (response.data.status) {
          setLoggedInUser(response.data.data.username);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, []);

  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/login', { username, password });
      if (response.status === 200) {
        setError('');
        setLoggedInUser(username);
        if (onLogin) {
          onLogin(); // Call the onLogin callback if provided
        }
      }
    } catch (err) {
      console.log('err:', err);
      setError('Invalid username or password');
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('/api/logout');
      setLoggedInUser(null);
      if (onLogout) {
        onLogout(); // Call the onLogout callback if provided
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <Box className={classes.root}>
      <Paper className={classes.paper} elevation={3}>
        {loggedInUser ? (
          <div>
            <Typography variant="h5" className={classes.title}>
              Welcome, {loggedInUser}!
            </Typography>
            <Button
              variant="contained"
              color="secondary"
              fullWidth
              onClick={handleLogout}
              className={classes.button}
            >
              Logout
            </Button>
          </div>
        ) : (
          <div>
            <Typography variant="h4" className={classes.title}>
              Login
            </Typography>
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && <Typography color="error">{error}</Typography>}
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handleLogin}
              className={classes.button}
            >
              Login
            </Button>
          </div>
        )}
      </Paper>
    </Box>
  );
};

export default Login; 