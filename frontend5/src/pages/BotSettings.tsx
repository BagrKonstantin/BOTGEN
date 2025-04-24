import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { endpoints } from '../config/api';
import { fetchWithAuth } from '../utils/api';
import { BotSetting } from '../types';

export default function BotSettings() {
    const { botId } = useParams<{ botId: string }>();
    const navigate = useNavigate();
    const [settings, setSettings] = useState<BotSetting>({
        name: '',
        token: '',
        greeting_message: '',
        notifications: {
            on_new_user: false,
            on_product_sold: false,
            on_out_of_stock: false,
        },
    });
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSettings = async () => {
            try {
                const response = await fetchWithAuth(endpoints.getBotSettings(Number(botId)));
                const data = await response.json();
                setSettings(data);
            } catch (error) {
                console.error('Error fetching bot settings:', error);
                setError('Failed to load bot settings');
            }
        };

        fetchSettings();
    }, [botId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        setError(null);

        try {
            const response = await fetchWithAuth(endpoints.saveBotSettings(Number(botId)), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings),
            });

            if (!response.ok) {
                throw new Error('Failed to save settings');
            }

            navigate('/bots');
        } catch (error) {
            console.error('Error saving settings:', error);
            setError('Failed to save settings');
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-2xl mx-auto">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h1 className="text-2xl font-bold mb-6">Bot Settings</h1>

                    {error && (
                        <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Bot Name
                            </label>
                            <input
                                type="text"
                                value={settings.name}
                                onChange={(e) => setSettings({ ...settings, name: e.target.value })}
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Bot Token
                            </label>
                            <input
                                type="text"
                                value={settings.token}
                                onChange={(e) => setSettings({ ...settings, token: e.target.value })}
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Greeting Message
                            </label>
                            <textarea
                                value={settings.greeting_message}
                                onChange={(e) => setSettings({ ...settings, greeting_message: e.target.value })}
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                rows={4}
                                required
                            />
                        </div>

                        <div className="space-y-4">
                            <h3 className="text-lg font-medium text-gray-700">Notifications</h3>

                            <div className="flex items-center">
                                <input
                                    type="checkbox"
                                    id="newUser"
                                    checked={settings.notifications.on_new_user}
                                    onChange={(e) =>
                                        setSettings({
                                            ...settings,
                                            notifications: {
                                                ...settings.notifications,
                                                on_new_user: e.target.checked,
                                            },
                                        })
                                    }
                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                />
                                <label htmlFor="newUser" className="ml-2 block text-sm text-gray-700">
                                    New User Notifications
                                </label>
                            </div>

                            <div className="flex items-center">
                                <input
                                    type="checkbox"
                                    id="productSold"
                                    checked={settings.notifications.on_product_sold}
                                    onChange={(e) =>
                                        setSettings({
                                            ...settings,
                                            notifications: {
                                                ...settings.notifications,
                                                on_product_sold: e.target.checked,
                                            },
                                        })
                                    }
                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                />
                                <label htmlFor="productSold" className="ml-2 block text-sm text-gray-700">
                                    Product Sold Notifications
                                </label>
                            </div>

                            <div className="flex items-center">
                                <input
                                    type="checkbox"
                                    id="outOfStock"
                                    checked={settings.notifications.on_out_of_stock}
                                    onChange={(e) =>
                                        setSettings({
                                            ...settings,
                                            notifications: {
                                                ...settings.notifications,
                                                on_out_of_stock: e.target.checked,
                                            },
                                        })
                                    }
                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                />
                                <label htmlFor="outOfStock" className="ml-2 block text-sm text-gray-700">
                                    Out of Stock Notifications
                                </label>
                            </div>
                        </div>

                        <div className="flex justify-end space-x-4">
                            <button
                                type="button"
                                onClick={() => navigate('/bots')}
                                className="px-4 py-2 text-gray-600 hover:text-gray-800"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={isSaving}
                                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-blue-300"
                            >
                                {isSaving ? 'Saving...' : 'Save Settings'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}