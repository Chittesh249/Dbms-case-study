import { useState } from 'react'
import { Box, ThemeProvider, createTheme } from '@mui/material'
import './App.css'
import Searchbar from './components/Searchbar/index.jsx';
import Sidebar from './components/Sidebar/index.jsx';
import Chat from './components/Chat/index.jsx';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#10a37f',
    },
  },
});

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleSendMessage = async (message) => {
    const newMessage = {
      text: message,
      isUser: true,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, newMessage]);
    
    try {
      // Add loading message
      const loadingMessage = {
        text: "Thinking...",
        isUser: false,
        timestamp: new Date(),
        isLoading: true,
      };
      setMessages(prev => [...prev, loadingMessage]);
      
      // Call backend API
      const response = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Remove loading message and add actual response
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.isLoading);
        return [...withoutLoading, {
          text: data.reply,
          isUser: false,
          timestamp: new Date(),
        }];
      });
      
    } catch (error) {
      console.error('Error calling backend:', error);
      
      // Remove loading message and add error response
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.isLoading);
        return [...withoutLoading, {
          text: `Sorry, I encountered an error: ${error.message}. Please make sure the backend server is running on http://localhost:8001`,
          isUser: false,
          timestamp: new Date(),
        }];
      });
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', height: '100vh' }}>
        <Sidebar />
        <Box sx={{ 
          flexGrow: 1, 
          display: 'flex', 
          flexDirection: 'column',
          marginLeft: '280px',
          position: 'relative'
        }}>
          <Chat messages={messages} />
          <Searchbar 
            onSendMessage={handleSendMessage}
            inputValue={inputValue}
            setInputValue={setInputValue}
          />
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App
