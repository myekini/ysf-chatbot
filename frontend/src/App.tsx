import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Paperclip, X, GraduationCap, ChevronRight } from 'lucide-react';
import { Button } from './components/ui/button';
import { Typewriter } from './components/ui/typewriter';
import { cn } from './lib/utils';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const YSJChatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.content }),
      });

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response || 'Sorry, I encountered an error.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(true); // Start typing effect for the new message
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      const systemMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.message || `File "${file.name}" uploaded successfully.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, systemMessage]);
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Error uploading file. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleQuickAction = (text: string) => {
    // We update input then send immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    // API Call logic extracted or duplicated for immediate send
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    })
    .then(res => res.json())
    .then(data => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response || 'Sorry, I encountered an error.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(true);
    })
    .catch(err => console.error(err))
    .finally(() => setIsLoading(false));
  };

  const clearChat = async () => {
    try {
      await fetch('/api/clear', { method: 'POST' });
      setMessages([]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-3 shadow-sm relative z-10">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          {/* Logo Section */}
          <div className="flex items-center gap-4 select-none">
            {/* Est. Block */}
            <div className="flex flex-col items-end justify-center h-full text-right leading-[0.9] text-foreground">
              <span className="text-[10px] font-medium opacity-80">Est.</span>
              <span className="text-xl font-bold tracking-tight">1841</span>
            </div>
            
            {/* Vertical Divider */}
            <div className="w-[1px] h-10 bg-foreground/20"></div>
            
            {/* Text Block */}
            <div className="flex flex-col justify-center">
              <div className="flex flex-col leading-none space-y-[2px] text-foreground">
                <span className="text-[15px] font-extrabold tracking-wide">YORK</span>
                <span className="text-[15px] font-extrabold tracking-wide">ST JOHN</span>
                <span className="text-[15px] font-extrabold tracking-wide">UNIVERSITY</span>
              </div>
              {/* Horizontal Line */}
              <div className="h-[1px] bg-foreground/20 w-full my-1.5"></div>
              {/* Subtitle */}
              <span className="text-xs font-medium tracking-widest uppercase text-muted-foreground">Student Assistant</span>
            </div>
          </div>

          <Button
            variant="ghost"
            size="sm"
            onClick={clearChat}
            className="text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
          >
            <X className="w-4 h-4 mr-2" />
            Clear Chat
          </Button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-4xl mx-auto flex flex-col">
          <div className="flex-1 overflow-y-auto custom-scrollbar px-6 py-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center px-4">
                <div className="w-24 h-24 rounded-full bg-secondary/50 flex items-center justify-center mb-6 animate-in zoom-in-50 duration-500">
                  <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center text-primary-foreground shadow-lg">
                    <GraduationCap className="w-8 h-8" />
                  </div>
                </div>
                <h2 className="text-2xl font-bold text-foreground mb-3">
                  Welcome to York St John
                </h2>
                <p className="text-muted-foreground max-w-md text-base leading-relaxed">
                  I'm your AI student assistant. Ask me about your <span className="text-primary font-medium">timetable</span>, <span className="text-primary font-medium">campus map</span>, or <span className="text-primary font-medium">student services</span>.
                </p>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-8 w-full max-w-lg">
                  <button 
                    onClick={() => handleQuickAction("Where can I find the library?")}
                    className="flex items-center justify-between p-4 rounded-xl border border-border bg-card hover:bg-secondary/50 transition-colors text-left group"
                  >
                    <span className="text-sm font-medium text-foreground">Where is the library?</span>
                    <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                  </button>
                  <button 
                    onClick={() => handleQuickAction("How do I submit my assignment?")}
                    className="flex items-center justify-between p-4 rounded-xl border border-border bg-card hover:bg-secondary/50 transition-colors text-left group"
                  >
                    <span className="text-sm font-medium text-foreground">Submit assignment</span>
                    <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message, index) => (
                  <div
                    key={message.id}
                    className={cn(
                      "flex gap-4",
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground flex-shrink-0">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}
                    <div
                      className={cn(
                        "max-w-[80%] rounded-lg px-4 py-3",
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-foreground'
                      )}
                    >
                      {message.role === 'assistant' ? (
                        <div className="text-sm">
                          <Typewriter 
                            text={message.content} 
                            speed={10} 
                            onComplete={() => {
                              scrollToBottom();
                              if (index === messages.length - 1) setIsTyping(false);
                            }} 
                          />
                        </div>
                      ) : (
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                      )}
                      <p className="text-xs opacity-70 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                    {message.role === 'user' && (
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-secondary text-secondary-foreground flex-shrink-0">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex gap-4 justify-start animate-in fade-in slide-in-from-bottom-2 duration-300">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground flex-shrink-0">
                      <Bot className="w-4 h-4" />
                    </div>
                    <div className="bg-muted text-foreground rounded-2xl px-4 py-3 shadow-sm border border-border/50">
                      <div className="flex items-center gap-3">
                        <div className="flex gap-1">
                          <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                          <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                          <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce"></span>
                        </div>
                        <span className="text-xs font-medium text-muted-foreground animate-pulse">
                          Searching Academic Documents...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          <div className="border-t border-border bg-card px-6 py-6">
            <div className="max-w-3xl mx-auto">
              <div className="flex items-center gap-2 bg-secondary/15 rounded-2xl p-2 focus-within:ring-1 focus-within:ring-primary/10 transition-all">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept=".pdf"
                  className="hidden"
                />
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => fileInputRef.current?.click()}
                  className="h-10 w-10 text-muted-foreground hover:text-primary hover:bg-transparent shrink-0"
                >
                  <Paperclip className="w-5 h-5" />
                </Button>
                
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a question..."
                  disabled={isLoading || isTyping}
                  className="flex-1 bg-transparent border-0 focus:ring-0 focus:outline-none px-2 py-2 text-base placeholder:text-muted-foreground/40"
                />

                <Button 
                  type="submit" 
                  size="icon"
                  onClick={handleSendMessage}
                  disabled={!input.trim() || isLoading || isTyping}
                  className={cn(
                    "h-10 w-10 rounded-xl transition-all duration-300 shrink-0",
                    input.trim() && !isLoading && !isTyping 
                      ? "bg-primary text-primary-foreground shadow-sm" 
                      : "bg-muted text-muted-foreground"
                  )}
                >
                  <Send className="w-5 h-5" />
                </Button>
              </div>
            </div>
            <div className="text-center mt-4 text-[11px] text-muted-foreground/80 leading-normal">
              <div className="pt-3 border-t border-border/40 w-full max-w-sm mx-auto">
                <p className="font-bold text-foreground/90">Designed & Built by Preowei Precious Elemson (240251549)</p>
                <p>MSc Data Science • Applied Research Project • 2025/2026 Academic Session</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YSJChatbot;
