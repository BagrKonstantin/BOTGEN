import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import Authorization from './pages/Authorization';
import BotList from './pages/BotList';
import Constructor from './pages/Constructor';
import Products from './pages/Products';
import BotSettings from './pages/BotSettings';

function PrivateRoute({ children }: { children: React.ReactNode }) {
    const token = useAuthStore((state) => state.accessToken);
    return token ? <>{children}</> : <Navigate to="/" />;
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Authorization />} />
                <Route path="/test" element={<h1>Test Page</h1>} />
                <Route
                    path="/bots"
                    element={
                        <PrivateRoute>
                            <BotList />
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/constructor/:botId"
                    element={
                        <PrivateRoute>
                            <Constructor />
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/products/:botId"
                    element={
                        <PrivateRoute>
                            <Products />
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/bot-settings/:botId"
                    element={
                        <PrivateRoute>
                            <BotSettings />
                        </PrivateRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;