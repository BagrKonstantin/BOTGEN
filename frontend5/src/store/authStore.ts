import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  temporalToken: string | null;
  accessToken: string | null;
  tokenType: string | null;
  setTemporalToken: (token: string) => void;
  setAccessToken: (token: string, type: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      temporalToken: null,
      accessToken: null,
      tokenType: null,
      setTemporalToken: (token) => set({ temporalToken: token }),
      setAccessToken: (token, type) => 
        set({ accessToken: token, tokenType: type, temporalToken: null }),
      clearAuth: () => 
        set({ temporalToken: null, accessToken: null, tokenType: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);