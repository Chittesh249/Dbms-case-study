import React from 'react';
import { Box, Typography, Paper, Avatar } from '@mui/material';
import { styled } from '@mui/material/styles';

const MessageContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  gap: theme.spacing(2),
  padding: theme.spacing(2),
  maxWidth: '100%',
  overflowY: 'auto',
  height: 'calc(100vh - 200px)',
}));

const MessageBubble = styled(Paper)(({ theme, isUser }) => ({
  padding: theme.spacing(2),
  maxWidth: '80%',
  alignSelf: isUser ? 'flex-end' : 'flex-start',
  backgroundColor: isUser ? theme.palette.primary.main : theme.palette.grey[100],
  color: isUser ? theme.palette.primary.contrastText : theme.palette.text.primary,
  borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
}));

const MessageHeader = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  marginBottom: 8,
});

export default function Chat({ messages }) {
  return (
    <MessageContainer>
      {messages.length === 0 ? (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            textAlign: 'center',
            color: 'text.secondary',
          }}
        >
          <Typography variant="h4" gutterBottom>
            How can I help you today?
          </Typography>
          <Typography variant="body1">
            Start a conversation by typing a message below.
          </Typography>
        </Box>
      ) : (
        messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              flexDirection: message.isUser ? 'row-reverse' : 'row',
              alignItems: 'flex-start',
              gap: 1,
            }}
          >
            <Avatar
              sx={{
                bgcolor: message.isUser ? 'primary.main' : 'grey.500',
                width: 32,
                height: 32,
                fontSize: '0.875rem',
              }}
            >
              {message.isUser ? 'U' : 'AI'}
            </Avatar>
            <MessageBubble isUser={message.isUser}>
              <MessageHeader>
                <Typography variant="subtitle2" fontWeight="bold">
                  {message.isUser ? 'You' : 'Assistant'}
                </Typography>
              </MessageHeader>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {message.text}
              </Typography>
            </MessageBubble>
          </Box>
        ))
      )}
    </MessageContainer>
  );
}
