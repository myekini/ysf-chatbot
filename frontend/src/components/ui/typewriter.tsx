import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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
  }, [text, speed]);

  return (
    <div className="prose prose-sm prose-neutral dark:prose-invert max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {displayedText + (!isComplete ? ' ▎' : '')}
      </ReactMarkdown>
    </div>
  );
};
