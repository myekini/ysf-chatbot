import React, { useState, useEffect } from 'react';

interface TypewriterProps {
  text: string;
  speed?: number;
  onComplete?: () => void;
}

export const Typewriter: React.FC<TypewriterProps> = ({ 
  text, 
  speed = 15, 
  onComplete 
}) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    // If text changes completely (new message), reset
    setDisplayedText('');
    setIsComplete(false);
    
    let index = 0;
    const intervalId = setInterval(() => {
      if (index < text.length) {
        setDisplayedText((prev) => prev + text.charAt(index));
        index++;
      } else {
        clearInterval(intervalId);
        setIsComplete(true);
        if (onComplete) onComplete();
      }
    }, speed);

    return () => clearInterval(intervalId);
  }, [text, speed, onComplete]);

  // If complete, just show full text to avoid any sync issues
  if (isComplete) {
    return <span className="whitespace-pre-wrap">{text}</span>;
  }

  return (
    <span className="whitespace-pre-wrap">
      {displayedText}
      <span className="animate-pulse">|</span>
    </span>
  );
};
