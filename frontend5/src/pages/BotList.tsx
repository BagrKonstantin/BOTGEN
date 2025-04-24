import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Edit, Trash2, Play, Square, Package, Settings } from 'lucide-react';
import { API_BASE_URL, endpoints } from '../config/api';
import { Bot } from '../types';
import { fetchWithAuth } from '../utils/api';
import { useAuthStore } from '../store/authStore';

export default function BotList() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [isNewBotModalOpen, setIsNewBotModalOpen] = useState(false);
  const [newBotName, setNewBotName] = useState('');
  const [newBotToken, setNewBotToken] = useState('');
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null);
  const navigate = useNavigate();
  // const { tokenType, accessToken } = useAuthStore();

  const fetchBots = async () => {
    try {
      const response = await fetchWithAuth(endpoints.allBots);
      const data = await response.json();
      setBots(data);
    } catch (error) {
      console.error('Error fetching bots:', error);
    }
  };

  useEffect(() => {
    fetchBots();
  }, []);

  const handleCreateBot = async () => {
    try {
      const response = await fetchWithAuth(endpoints.newBot(newBotToken), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newBotName }),
      });
      const newBot = await response.json();
      // setBots([...bots, newBot]);
      setIsNewBotModalOpen(false);
      setNewBotName('');
      setNewBotToken('');
      fetchBots();
    } catch (error) {
      console.error('Error creating bot:', error);
    }
  };

  const handleDeleteBot = async (botId: number) => {
    try {
      await fetchWithAuth(endpoints.deleteBot(botId), {
        method: 'DELETE',
      });
      setBots(bots.filter((bot) => bot.bot_id !== botId));
      setDeleteConfirmId(null);
    } catch (error) {
      console.error('Error deleting bot:', error);
    }
  };

  const handleLaunchStop = async (botId: number, isLaunched: boolean) => {
    try {
      const endpoint = endpoints.launchBot(botId);
      await fetchWithAuth(endpoint, {
        method: 'POST',
      });
      await fetchBots();
    } catch (error) {
      console.error('Error updating bot status:', error);
    }
  };

  return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Your Bots</h1>
            <button
                onClick={() => setIsNewBotModalOpen(true)}
                className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
            >
              <Plus size={20} /> New Bot
            </button>
          </div>

          <div className="grid gap-4">
            {bots.map((bot) => (
                <div
                    key={bot.bot_id}
                    className="bg-white p-4 rounded-lg shadow-md flex items-center justify-between"
                >
                  <span className="text-xl font-medium">{bot.name}</span>
                  <div className="flex items-center gap-2">
                    <button
                        onClick={() => navigate(`/products/${bot.bot_id}`)}
                        className="p-2 text-gray-600 hover:text-blue-500"
                        title="Products"
                    >
                      <Package size={20} />
                    </button>
                    <button
                        onClick={() => navigate(`/constructor/${bot.bot_id}`)}
                        className="p-2 text-gray-600 hover:text-blue-500"
                        title="Constructor"
                    >
                      <Edit size={20} />
                    </button>
                    <button
                        onClick={() => navigate(`/bot-settings/${bot.bot_id}`)}
                        className="p-2 text-gray-600 hover:text-blue-500"
                        title="Settings"
                    >
                      <Settings size={20} />
                    </button>
                    <button
                        onClick={() => handleLaunchStop(bot.bot_id, bot.is_launched)}
                        className={`p-2 ${
                            bot.is_launched
                                ? 'text-red-500 hover:text-red-600'
                                : 'text-green-500 hover:text-green-600'
                        }`}
                        title={bot.is_launched ? 'Stop Bot' : 'Start Bot'}
                    >
                      {bot.is_launched ? <Square size={20} /> : <Play size={20} />}
                    </button>
                    <button
                        onClick={() => setDeleteConfirmId(bot.bot_id)}
                        className="p-2 text-gray-600 hover:text-red-500"
                        title="Delete Bot"
                    >
                      <Trash2 size={20} />
                    </button>
                  </div>
                </div>
            ))}
          </div>

          {/* New Bot Modal */}
          {isNewBotModalOpen && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="bg-white p-6 rounded-lg w-96">
                  <h2 className="text-2xl font-bold mb-4">Create New Bot</h2>
                  <div className="space-y-4">
                    <input
                        type="text"
                        value={newBotName}
                        onChange={(e) => setNewBotName(e.target.value)}
                        placeholder="Bot Name"
                        className="w-full px-4 py-2 border rounded-md"
                    />
                    <input
                        type="text"
                        value={newBotToken}
                        onChange={(e) => setNewBotToken(e.target.value)}
                        placeholder="Bot Token"
                        className="w-full px-4 py-2 border rounded-md"
                    />
                    <div className="flex justify-end gap-2">
                      <button
                          onClick={() => setIsNewBotModalOpen(false)}
                          className="px-4 py-2 text-gray-600 hover:text-gray-800"
                      >
                        Cancel
                      </button>
                      <button
                          onClick={handleCreateBot}
                          disabled={!newBotName || !newBotToken}
                          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-blue-300"
                      >
                        Create Bot
                      </button>
                    </div>
                  </div>
                </div>
              </div>
          )}

          {/* Delete Confirmation Modal */}
          {deleteConfirmId !== null && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="bg-white p-6 rounded-lg w-96">
                  <h2 className="text-2xl font-bold mb-4">Confirm Deletion</h2>
                  <p className="mb-4">Are you sure you want to delete this bot?</p>
                  <div className="flex justify-end gap-2">
                    <button
                        onClick={() => setDeleteConfirmId(null)}
                        className="px-4 py-2 text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <button
                        onClick={() => handleDeleteBot(deleteConfirmId)}
                        className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
          )}
        </div>
      </div>
  );
}