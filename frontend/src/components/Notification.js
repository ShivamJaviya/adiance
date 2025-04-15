import React from 'react';
import { useAppContext } from '../utils/AppContext';

const Notification = () => {
  const { notification } = useAppContext();
  
  if (!notification) return null;
  
  const { message, type } = notification;
  
  const bgColor = {
    info: 'bg-primary-blue',
    success: 'bg-success',
    warning: 'bg-warning',
    error: 'bg-error',
  }[type] || 'bg-primary-blue';
  
  return (
    <div className={`fixed top-4 right-4 ${bgColor} text-white px-4 py-2 rounded-md shadow-lg z-50 micro-interaction`}>
      {message}
    </div>
  );
};

export default Notification;
