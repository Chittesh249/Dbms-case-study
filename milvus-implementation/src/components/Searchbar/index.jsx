import * as React from 'react';
import { Box, TextField, IconButton, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { styled } from '@mui/material/styles';

const InputContainer = styled(Paper)(({ theme }) => ({
  position: 'fixed',
  bottom: 20,
  left: '50%',
  transform: 'translateX(-50%)',
  width: 'calc(100% - 320px)',
  maxWidth: '800px',
  padding: theme.spacing(1),
  display: 'flex',
  alignItems: 'flex-end',
  gap: theme.spacing(1),
  zIndex: 1000,
  boxShadow: theme.shadows[8],
}));

export default function Searchbar({ onSendMessage, inputValue, setInputValue }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <InputContainer elevation={3}>
      <TextField
        fullWidth
        multiline
        maxRows={4}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter the Message ..."
        variant="outlined"
        sx={{
          '& .MuiOutlinedInput-root': {
            borderRadius: 2,
            '& fieldset': {
              border: 'none',
            },
          },
        }}
      />
      <IconButton
        color="primary"
        onClick={handleSubmit}
        disabled={!inputValue.trim()}
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          '&:hover': {
            bgcolor: 'primary.dark',
          },
          '&:disabled': {
            bgcolor: 'grey.300',
            color: 'grey.500',
          },
        }}
      >
        <SendIcon />
      </IconButton>
    </InputContainer>
  );
}
