import React from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import NewsList from './components/NewsList';
import UploadCsv from './components/UploadCsv';
import Navigation from './components/Navigation';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ainews" element={<NewsList />} />
          <Route path="/upload" element={<UploadCsv />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App; 