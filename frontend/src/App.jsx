import React from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import NewsList from './components/NewsList';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NewsList />
    </ThemeProvider>
  );
}

export default App; 