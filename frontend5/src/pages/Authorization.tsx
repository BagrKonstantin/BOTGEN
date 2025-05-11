import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { API_BASE_URL, endpoints } from '../config/api';
import { useAuthStore } from '../store/authStore';
import {AlertCircle} from "lucide-react";

export default function Authorization() {
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { setTemporalToken, setAccessToken, temporalToken } = useAuthStore();
  const hasLoggedIn = useRef(false);
  const [error, setError] = useState<string | null>(null);
  const [telegram, setTelegram] = useState<string | null>(null);


  const handleLogin = async (user) => {
    try {
      console.log(user);
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}${endpoints.login(user)}`, {
        method: 'POST',
      })

      if (!response.ok) {
        setError((await response.json()).detail);
        setIsLoading(false);
      } else {
        setError(null)
      }

      const data = await response.json();
      setTemporalToken(data.token);
      setTelegram("check")
    } catch (error) {
      console.error('Login error:', error);
      setIsLoading(false);
    }
  };
  useEffect(() => {
    const urlUsername = searchParams.get('username');
    if (useAuthStore.getState().accessToken){
      navigate('/bots');
      return;
    }
    if (urlUsername && !hasLoggedIn.current) {
      hasLoggedIn.current = true;
      setTelegram("check")
      setUsername(urlUsername);
      handleLogin(urlUsername);
    }
  }, [searchParams]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (temporalToken) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(
            `${API_BASE_URL}${endpoints.checkLoginStatus(temporalToken)}`
          );
          const data = await response.json();
          if (data.access_token) {
            setAccessToken(data.access_token, data.token_type);
            navigate('/bots');
          }
        } catch (error) {
          console.error('Status check error:', error);
          setIsLoading(false);
        }
      }, 2000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [temporalToken, navigate, setAccessToken]);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        {error && (
            <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md flex items-center gap-2">
              <AlertCircle size={20} />
              <p>Use <a target="_blank" rel="noopener noreferrer" href="https://t.me/botgen_official_bot">@botgen_official_bot</a> to register</p>
            </div>
        )}
        {telegram && (
            <div className="mb-4 p-4 bg-green-100 text-green-700 rounded-md flex items-center gap-2">
              <AlertCircle size={20} />
              {'Click "Authorize" in Telegram bot'}
            </div>
        )}
        <h1 className="text-2xl font-bold mb-6 text-center">BotGen Login</h1>
        <div className="space-y-4">
          <input
            type="text"
            value={username}
            disabled={isLoading}
            onChange={(e) => {
              const value = e.target.value;
              if (value.startsWith('@')) {
                setUsername(value.slice(1));
              } else {
                setUsername(value);
              }
            }}
            placeholder="username"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={(e) => {

            handleLogin(username);
          }}
            disabled={isLoading || !username}
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 disabled:bg-blue-300"
          >
            {isLoading ? 'Checking...' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  );
}