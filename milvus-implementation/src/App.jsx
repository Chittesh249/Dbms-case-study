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

  const handleSendMessage = (message) => {
    const newMessage = {
      text: message,
      isUser: true,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, newMessage]);
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        text: `I received your message: "${message}". This is a simulated response from the AI assistant.`,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
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
