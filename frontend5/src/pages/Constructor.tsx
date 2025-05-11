import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Plus,
  Save,
  ArrowLeft,
  Image as ImageIcon,
  Type,
  Package,
  X,
  Edit2,
  Trash2,
  ArrowUp,
  ArrowDown,
  MessageSquare,
  AlertCircle,
} from 'lucide-react';
import { API_BASE_URL, endpoints } from '../config/api';
import { Stage, BotData, Button, Dialog } from '../types';
import { fetchWithAuth } from '../utils/api';

export default function Constructor() {
  const { botId } = useParams<{ botId: string }>();
  const navigate = useNavigate();
  const [dialogs, setDialogs] = useState<Record<string, Dialog>>({});
  const [dialogOrder, setDialogOrder] = useState<string[]>([]);
  const [selectedDialog, setSelectedDialog] = useState<string | null>(null);
  const [selectedStage, setSelectedStage] = useState<string | null>(null);
  const [editingDialogName, setEditingDialogName] = useState<string | null>(null);
  const [editingStageName, setEditingStageName] = useState<string | null>(null);
  const [newName, setNewName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean | null>(null);

  useEffect(() => {
    const fetchBotData = async () => {
      try {
        const response = await fetchWithAuth(endpoints.getBot(Number(botId)));
        const data: BotData = await response.json();
        setDialogs(data.dialogs || {});
        setDialogOrder(Object.keys(data.dialogs || {}));
      } catch (error) {
        console.error('Error fetching bot data:', error);
      }
    };

    if (botId) {
      fetchBotData();
    }
  }, [botId]);

  const handleAddDialog = () => {
    setSuccess(false);
    const newDialogId = `dialog-${dialogOrder.length}`;
    setDialogs({
      ...dialogs,
      [newDialogId]: {
        stages: {},
      },
    });
    setDialogOrder([...dialogOrder, newDialogId]);
  };

  const handleAddStage = (dialogId: string) => {
    setSuccess(false);
    const dialog = dialogs[dialogId];
    const newStageId = `stage-${Object.keys(dialog.stages).length}`;
    setDialogs({
      ...dialogs,
      [dialogId]: {
        ...dialog,
        stages: {
          ...dialog.stages,
          [newStageId]: {
            type: 'text',
            text: '',
            keyboard: {
              back_button: false,
              buttons: {},
            },
          },
        },
      },
    });
  };

  const handleDeleteDialog = (dialogId: string) => {
    setSuccess(false);
    console.log(dialogs);
    console.log(dialogOrder);
    delete dialogs[dialogId];
    dialogOrder.splice(dialogOrder.indexOf(dialogId), 1);
    // delete dialogOrder[dialogOrder.indexOf(dialogId)];
    // dialogOrder.filter(item => item !== dialogId)
    console.log(dialogs);
    console.log(dialogOrder);
    setSelectedDialog(null);
    setDialogs({
      ...dialogs
    });

  };

  const handleDeleteStage = (dialogId: string, stageId: string) => {
    setSuccess(false);
    const stages = dialogs[dialogId].stages;
    delete stages[stageId];
    setDialogs({
      ...dialogs
    });
  };

  const handleMoveDialog = (index: number, direction: 'up' | 'down') => {
    setSuccess(false);
    const newOrder = [...dialogOrder];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    [newOrder[index], newOrder[newIndex]] = [newOrder[newIndex], newOrder[index]];
    setDialogOrder(newOrder);
  };

  const handleMoveStage = (
      dialogId: string,
      stageId: string,
      direction: 'up' | 'down'
  ) => {
    setSuccess(false);
    const dialog = dialogs[dialogId];
    const stageOrder = Object.keys(dialog.stages);
    const currentIndex = stageOrder.indexOf(stageId);
    const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;

    const newStages = stageOrder.reduce((acc, curr, idx) => {
      if (idx === currentIndex) {
        acc[stageOrder[newIndex]] = dialog.stages[stageOrder[newIndex]];
      } else if (idx === newIndex) {
        acc[stageOrder[currentIndex]] = dialog.stages[stageOrder[currentIndex]];
      } else {
        acc[curr] = dialog.stages[curr];
      }
      return acc;
    }, {} as Record<string, Stage>);

    setDialogs({
      ...dialogs,
      [dialogId]: {
        ...dialog,
        stages: newStages,
      },
    });
  };

  const handleDialogNameChange = (oldName: string) => {
    setSuccess(false);
    if (!newName || newName === oldName) {
      setEditingDialogName(null);
      setNewName('');
      setError(null);
      return;
    }

    if (dialogOrder.includes(newName)) {
      setError('A dialog with this name already exists');
      return;
    }

    const updatedDialogs = { ...dialogs };
    const dialog = updatedDialogs[oldName];
    delete updatedDialogs[oldName];
    updatedDialogs[newName] = dialog;

    setDialogs(updatedDialogs);
    setDialogOrder(dialogOrder.map((id) => (id === oldName ? newName : id)));
    if (selectedDialog === oldName) {
      setSelectedDialog(newName);
    }
    setEditingDialogName(null);
    setNewName('');
    setError(null);
  };

  const handleStageNameChange = (dialogId: string, oldName: string) => {
    setSuccess(false);
    if (!newName || newName === oldName) {
      setEditingStageName(null);
      setNewName('');
      setError(null);
      return;
    }

    if (Object.keys(dialogs[dialogId].stages).includes(newName)) {
      setError('A stage with this name already exists in this dialog');
      return;
    }

    const dialog = dialogs[dialogId];
    const updatedStages = { ...dialog.stages };
    const stage = updatedStages[oldName];
    delete updatedStages[oldName];
    updatedStages[newName] = stage;

    Object.values(updatedStages).forEach((stage) => {
      Object.entries(stage.keyboard.buttons).forEach(([buttonId, button]) => {
        if (button.to === oldName) {
          stage.keyboard.buttons[buttonId] = { ...button, to: newName };
        }
        if (button.if?.stage === oldName) {
          stage.keyboard.buttons[buttonId] = {
            ...button,
            if: { ...button.if, stage: newName },
          };
        }
      });
    });

    setDialogs({
      ...dialogs,
      [dialogId]: {
        ...dialog,
        stages: updatedStages,
      },
    });

    if (selectedStage === oldName) {
      setSelectedStage(newName);
    }
    setEditingStageName(null);
    setNewName('');
    setError(null);
  };

  const handleStageTypeChange = (
      dialogId: string,
      stageId: string,
      type: Stage['type']
  ) => {
    setSuccess(false);
    const newStage: Stage = {
      type,
      keyboard: dialogs[dialogId].stages[stageId].keyboard,
      ...(type === 'text' && { text: '' }),
      ...(type === 'image' && { text: '', image: '' }),
      ...(type === 'product' && {
        product: { title: '', description: '', price: 0 },
      }),
    };
    setDialogs({
      ...dialogs,
      [dialogId]: {
        ...dialogs[dialogId],
        stages: {
          ...dialogs[dialogId].stages,
          [stageId]: newStage,
        },
      },
    });
  };

  const getImageUrl = (imageId: string) => {
    return `${API_BASE_URL}${endpoints.getImage(Number(botId), imageId)}`;
  };

  // const getImage = async(
  //     imageId: string,
  // ) =>
  // {
  //   const response = await fetchWithAuth(endpoints.getImage(Number(botId), imageId), {
  //     method: 'GET',
  //   });
  //   await response.blob();
  // }

  const handleImageUpload = async (
      event: React.ChangeEvent<HTMLInputElement>,
      dialogId: string,
      stageId: string
  ) => {
    setSuccess(false);
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetchWithAuth(endpoints.uploadImage(Number(botId)), {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      const stage = dialogs[dialogId].stages[stageId] as ImageStage;
      setDialogs({
        ...dialogs,
        [dialogId]: {
          ...dialogs[dialogId],
          stages: {
            ...dialogs[dialogId].stages,
            [stageId]: { ...stage, image: data.image_id },
          },
        },
      });
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  const handleAddButton = (dialogId: string, stageId: string) => {
    setSuccess(false);
    const stage = dialogs[dialogId].stages[stageId];
    const buttonId = `option-${Object.keys(stage.keyboard.buttons).length}`;
    const newButton: Button = {
      text: 'New Button',
      to: '',
    };
    setDialogs({
      ...dialogs,
      [dialogId]: {
        ...dialogs[dialogId],
        stages: {
          ...dialogs[dialogId].stages,
          [stageId]: {
            ...stage,
            keyboard: {
              ...stage.keyboard,
              buttons: {
                ...stage.keyboard.buttons,
                [buttonId]: newButton,
              },
            },
          },
        },
      },
    });
  };

  const handleButtonConditionChange = (
      dialogId: string,
      stageId: string,
      buttonId: string,
      hasCondition: boolean
  ) => {
    setSuccess(false);
    const button = dialogs[dialogId].stages[stageId].keyboard.buttons[buttonId];

    if (hasCondition) {
      setDialogs({
        ...dialogs,
        [dialogId]: {
          ...dialogs[dialogId],
          stages: {
            ...dialogs[dialogId].stages,
            [stageId]: {
              ...dialogs[dialogId].stages[stageId],
              keyboard: {
                ...dialogs[dialogId].stages[stageId].keyboard,
                buttons: {
                  ...dialogs[dialogId].stages[stageId].keyboard.buttons,
                  [buttonId]: {
                    ...button,
                    if: {
                      stage: '',
                      equals: '',
                      to: button.to || ''
                    }
                  }
                }
              }
            }
          }
        }
      });
    } else {
      const { if: _, ...buttonWithoutCondition } = button;
      setDialogs({
        ...dialogs,
        [dialogId]: {
          ...dialogs[dialogId],
          stages: {
            ...dialogs[dialogId].stages,
            [stageId]: {
              ...dialogs[dialogId].stages[stageId],
              keyboard: {
                ...dialogs[dialogId].stages[stageId].keyboard,
                buttons: {
                  ...dialogs[dialogId].stages[stageId].keyboard.buttons,
                  [buttonId]: buttonWithoutCondition
                }
              }
            }
          }
        }
      });
    }
  };

  const handleSaveBot = async () => {
    try {
      const orderedDialogs = dialogOrder.reduce((acc, dialogId) => {
        acc[dialogId] = dialogs[dialogId];
        return acc;
      }, {} as Record<string, Dialog>);

      await fetchWithAuth(endpoints.saveBot(Number(botId)), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dialogs: orderedDialogs }),
      });
      setSuccess(true)
      // navigate('/bots');
    } catch (error) {
      console.error('Error saving bot:', error);
    }
  };

  return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-6xl mx-auto">
          {error && (
              <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md flex items-center gap-2">
                <AlertCircle size={20} />
                {error}
              </div>
          )}
          {success && (
              <div className="mb-4 p-4 bg-green-100 text-green-700 rounded-md flex items-center gap-2">
                <AlertCircle size={20} />
                {'Bot is saved'}
              </div>
          )}
          <div className="flex justify-between items-center mb-8">
            <button
                onClick={() => navigate('/bots')}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
            >
              <ArrowLeft size={20} /> Back to Bots
            </button>
            <div className="flex gap-4">
              <button
                  onClick={handleAddDialog}
                  className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              >
                <Plus size={20} /> Add Dialog
              </button>
              <button
                  onClick={handleSaveBot}
                  className="flex items-center gap-2 bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
              >
                <Save size={20} /> Save Bot
              </button>
            </div>
          </div>

          <div className="grid grid-cols-4 gap-4">
            {/* Dialogs and Stages List */}
            <div className="col-span-1 bg-white rounded-lg shadow-md p-4 h-fit">
              <h2 className="text-xl font-bold mb-4">Dialogs</h2>
              <div className="space-y-4">
                {dialogOrder.map((dialogId, index) => (
                    <div key={dialogId} className="space-y-2">
                      <div
                          className={`p-2 rounded-md ${
                              selectedDialog === dialogId ? 'bg-blue-50' : ''
                          }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <MessageSquare size={16} />
                            {editingDialogName === dialogId ? (
                                <input
                                    type="text"
                                    value={newName}
                                    onChange={(e) => setNewName(e.target.value)}
                                    onBlur={() => handleDialogNameChange(dialogId)}
                                    onKeyDown={(e) => {
                                      if (e.key === 'Enter') {
                                        handleDialogNameChange(dialogId);
                                      }
                                    }}
                                    className="w-full px-2 py-1 border rounded"
                                    autoFocus
                                />
                            ) : (
                                <span
                                    className="cursor-pointer"
                                    onClick={() => setSelectedDialog(dialogId)}
                                >
                            {dialogId}
                          </span>
                            )}
                          </div>
                          <div className="flex items-center gap-1">
                            {index > 0 && (
                                <button
                                    onClick={() => handleMoveDialog(index, 'up')}
                                    className="p-1 text-gray-500 hover:text-blue-500"
                                >
                                  <ArrowUp size={14} />
                                </button>
                            )}
                            {index < dialogOrder.length - 1 && (
                                <button
                                    onClick={() => handleMoveDialog(index, 'down')}
                                    className="p-1 text-gray-500 hover:text-blue-500"
                                >
                                  <ArrowDown size={14} />
                                </button>
                            )}
                            {editingDialogName !== dialogId && (
                                <button
                                    onClick={() => {
                                      setEditingDialogName(dialogId);
                                      setNewName(dialogId);
                                    }}
                                    className="p-1 text-gray-500 hover:text-blue-500"
                                >
                                  <Edit2 size={14} />
                                </button>
                            )}
                            {editingDialogName !== dialogId && (
                                <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleDeleteDialog(dialogId);
                                    }}
                                    className="p-1 text-gray-500 hover:text-blue-500"
                                >
                                  <Trash2 size={12} />
                                </button>
                            )}
                          </div>
                        </div>
                        {selectedDialog === dialogId && (
                            <div className="mt-2 pl-6 space-y-2">
                              <button
                                  onClick={() => handleAddStage(dialogId)}
                                  className="flex items-center gap-2 text-sm text-blue-500 hover:text-blue-600"
                              >
                                <Plus size={14} /> Add Stage
                              </button>
                              {Object.entries(dialogs[dialogId].stages).map(
                                  ([stageId, stage], stageIndex) => (
                                      <div
                                          key={stageId}
                                          onClick={() => setSelectedStage(stageId)}
                                          className={`p-2 rounded-md cursor-pointer flex items-center justify-between ${
                                              selectedStage === stageId
                                                  ? 'bg-blue-100'
                                                  : 'hover:bg-gray-100'
                                          }`}
                                      >
                                        <div className="flex items-center gap-2">
                                          {stage.type === 'text' && <Type size={14} />}
                                          {stage.type === 'image' && (
                                              <ImageIcon size={14} />
                                          )}
                                          {stage.type === 'product' && (
                                              <Package size={14} />
                                          )}
                                          {editingStageName === stageId ? (
                                              <input
                                                  type="text"
                                                  value={newName}
                                                  onChange={(e) => setNewName(e.target.value)}
                                                  onBlur={() =>
                                                      handleStageNameChange(dialogId, stageId)
                                                  }
                                                  onKeyDown={(e) => {
                                                    if (e.key === 'Enter') {
                                                      handleStageNameChange(dialogId, stageId);
                                                    }
                                                  }}
                                                  className="w-full px-2 py-1 border rounded"
                                                  autoFocus
                                              />
                                          ) : (
                                              <span>{stageId}</span>
                                          )}
                                        </div>
                                        <div className="flex items-center gap-1">
                                          {stageIndex > 0 && (
                                              <button
                                                  onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleMoveStage(dialogId, stageId, 'up');
                                                  }}
                                                  className="p-1 text-gray-500 hover:text-blue-500"
                                              >
                                                <ArrowUp size={12} />
                                              </button>
                                          )}
                                          {stageIndex <
                                              Object.keys(dialogs[dialogId].stages).length -
                                              1 && (
                                                  <button
                                                      onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleMoveStage(dialogId, stageId, 'down');
                                                      }}
                                                      className="p-1 text-gray-500 hover:text-blue-500"
                                                  >
                                                    <ArrowDown size={12} />
                                                  </button>
                                              )}
                                          {editingStageName !== stageId && (
                                              <button
                                                  onClick={(e) => {
                                                    e.stopPropagation();
                                                    setEditingStageName(stageId);
                                                    setNewName(stageId);
                                                  }}
                                                  className="p-1 text-gray-500 hover:text-blue-500"
                                              >
                                                <Edit2 size={12} />
                                              </button>
                                          )}
                                          {editingStageName !== stageId && (
                                              <button
                                                  onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleDeleteStage(dialogId, stageId);
                                                  }}
                                                  className="p-1 text-gray-500 hover:text-blue-500"
                                              >
                                                <Trash2 size={12} />
                                              </button>
                                          )}
                                        </div>
                                      </div>
                                  )
                              )}
                            </div>
                        )}
                      </div>
                    </div>
                ))}
              </div>
            </div>

            {/* Stage Editor */}
            {selectedDialog &&
                selectedStage &&
                dialogs[selectedDialog]?.stages[selectedStage] && (
                    <div className="col-span-3 bg-white rounded-lg shadow-md p-6">
                      <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Stage Type
                        </label>
                        <select
                            value={dialogs[selectedDialog].stages[selectedStage].type}
                            onChange={(e) =>
                                handleStageTypeChange(
                                    selectedDialog,
                                    selectedStage,
                                    e.target.value as Stage['type']
                                )
                            }
                            className="w-full p-2 border rounded-md"
                        >
                          <option value="text">Text</option>
                          <option value="image">Image</option>
                          <option value="product">Product</option>
                        </select>
                      </div>

                      {/* Stage Content */}
                      {dialogs[selectedDialog].stages[selectedStage].type === 'text' && (
                          <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Text Content
                            </label>
                            <textarea
                                value={
                                  (dialogs[selectedDialog].stages[selectedStage] as any).text
                                }
                                onChange={(e) =>
                                    setDialogs({
                                      ...dialogs,
                                      [selectedDialog]: {
                                        ...dialogs[selectedDialog],
                                        stages: {
                                          ...dialogs[selectedDialog].stages,
                                          [selectedStage]: {
                                            ...dialogs[selectedDialog].stages[selectedStage],
                                            text: e.target.value,
                                          },
                                        },
                                      },
                                    })
                                }
                                className="w-full p-2 border rounded-md h-32"
                            />
                          </div>
                      )}

                      {dialogs[selectedDialog].stages[selectedStage].type ===
                          'image' && (
                              <div className="mb-6 space-y-4">
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Text Content
                                  </label>
                                  <textarea
                                      value={
                                        (dialogs[selectedDialog].stages[selectedStage] as any)
                                            .text
                                      }
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[selectedStage],
                                                  text: e.target.value,
                                                },
                                              },
                                            },
                                          })
                                      }
                                      className="w-full p-2 border rounded-md h-32"
                                  />
                                </div>
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Image
                                  </label>
                                  <img
                                      src={getImageUrl((dialogs[selectedDialog].stages[selectedStage] as any).image)}
                                      alt="Stage"
                                      className="max-w-md rounded-lg shadow-md"
                                      // key={stage.image} // Add key to force re-render when image changes
                                  />
                                  <input
                                      type="file"
                                      accept="image/*"
                                      onChange={(e) =>
                                          handleImageUpload(e, selectedDialog, selectedStage)
                                      }
                                      className="w-full p-2 border rounded-md"
                                  />
                                </div>
                              </div>
                          )}

                      {dialogs[selectedDialog].stages[selectedStage].type ===
                          'product' && (
                              <div className="mb-6 space-y-4">
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Title
                                  </label>
                                  <input
                                      type="text"
                                      value={
                                          (dialogs[selectedDialog].stages[selectedStage] as any)
                                              .product?.title || ''
                                      }
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[selectedStage],
                                                  product: {
                                                    ...(dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ] as any).product,
                                                    title: e.target.value,
                                                  },
                                                },
                                              },
                                            },
                                          })
                                      }
                                      className="w-full p-2 border rounded-md"
                                  />
                                </div>
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Description
                                  </label>
                                  <textarea
                                      value={
                                          (dialogs[selectedDialog].stages[selectedStage] as any)
                                              .product?.description || ''
                                      }
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[selectedStage],
                                                  product: {
                                                    ...(dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ] as any).product,
                                                    description: e.target.value,
                                                  },
                                                },
                                              },
                                            },
                                          })
                                      }
                                      className="w-full p-2 border rounded-md h-32"
                                  />
                                </div>
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Price
                                  </label>
                                  <input
                                      type="number"
                                      value={
                                          (dialogs[selectedDialog].stages[selectedStage] as any)
                                              .product?.price || 0
                                      }
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[selectedStage],
                                                  product: {
                                                    ...(dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ] as any).product,
                                                    price: parseFloat(e.target.value),
                                                  },
                                                },
                                              },
                                            },
                                          })
                                      }
                                      className="w-full p-2 border rounded-md"
                                  />
                                </div>
                                <div>
                                  <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Image URL (optional)
                                  </label>
                                  <input
                                      type="text"
                                      value={
                                          (dialogs[selectedDialog].stages[selectedStage] as any)
                                              .product?.image_url || ''
                                      }
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[selectedStage],
                                                  product: {
                                                    ...(dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ] as any).product,
                                                    image_url: e.target.value,
                                                  },
                                                },
                                              },
                                            },
                                          })
                                      }
                                      className="w-full p-2 border rounded-md"
                                  />
                                </div>
                              </div>
                          )}

                      {/* Keyboard Section */}
                      <div className="border-t pt-6">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-lg font-medium">Keyboard</h3>
                          <button
                              onClick={() => handleAddButton(selectedDialog, selectedStage)}
                              className="flex items-center gap-2 text-blue-500 hover:text-blue-600"
                          >
                            <Plus size={16} /> Add Button
                          </button>
                        </div>

                        <div className="mb-4">
                          <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={
                                  dialogs[selectedDialog].stages[selectedStage].keyboard
                                      .back_button
                                }
                                onChange={(e) =>
                                    setDialogs({
                                      ...dialogs,
                                      [selectedDialog]: {
                                        ...dialogs[selectedDialog],
                                        stages: {
                                          ...dialogs[selectedDialog].stages,
                                          [selectedStage]: {
                                            ...dialogs[selectedDialog].stages[selectedStage],
                                            keyboard: {
                                              ...dialogs[selectedDialog].stages[selectedStage]
                                                  .keyboard,
                                              back_button: e.target.checked,
                                            },
                                          },
                                        },
                                      },
                                    })
                                }
                                className="rounded"
                            />
                            <span className="text-sm">Add back button</span>
                          </label>
                        </div>

                        <div className="space-y-4">
                          {Object.entries(
                              dialogs[selectedDialog].stages[selectedStage].keyboard
                                  .buttons
                          ).map(([buttonId, button]) => (
                              <div
                                  key={buttonId}
                                  className="space-y-4 p-4 border rounded-md"
                              >
                                <div className="flex items-center gap-4">
                                  <input
                                      type="text"
                                      value={button.text}
                                      onChange={(e) =>
                                          setDialogs({
                                            ...dialogs,
                                            [selectedDialog]: {
                                              ...dialogs[selectedDialog],
                                              stages: {
                                                ...dialogs[selectedDialog].stages,
                                                [selectedStage]: {
                                                  ...dialogs[selectedDialog].stages[
                                                      selectedStage
                                                      ],
                                                  keyboard: {
                                                    ...dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ].keyboard,
                                                    buttons: {
                                                      ...dialogs[selectedDialog].stages[
                                                          selectedStage
                                                          ].keyboard.buttons,
                                                      [buttonId]: {
                                                        ...button,
                                                        text: e.target.value,
                                                      },
                                                    },
                                                  },
                                                },
                                              },
                                            },
                                          })
                                      }
                                      placeholder="Button Text"
                                      className="flex-1 p-2 border rounded-md"
                                  />

                                  <label className="flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        checked={!!button.if}
                                        onChange={(e) =>
                                            handleButtonConditionChange(
                                                selectedDialog,
                                                selectedStage,
                                                buttonId,
                                                e.target.checked
                                            )
                                        }
                                        className="rounded"
                                    />
                                    <span className="text-sm">Add Condition</span>
                                  </label>

                                  <button
                                      onClick={() => {
                                        const newButtons = {
                                          ...dialogs[selectedDialog].stages[selectedStage]
                                              .keyboard.buttons,
                                        };
                                        delete newButtons[buttonId];
                                        setDialogs({
                                          ...dialogs,
                                          [selectedDialog]: {
                                            ...dialogs[selectedDialog],
                                            stages: {
                                              ...dialogs[selectedDialog].stages,
                                              [selectedStage]: {
                                                ...dialogs[selectedDialog].stages[
                                                    selectedStage
                                                    ],
                                                keyboard: {
                                                  ...dialogs[selectedDialog].stages[
                                                      selectedStage
                                                      ].keyboard,
                                                  buttons: newButtons,
                                                },
                                              },
                                            },
                                          },
                                        });
                                      }}
                                      className="p-2 text-red-500 hover:text-red-600"
                                  >
                                    <X size={20} />
                                  </button>
                                </div>

                                {button.if && (
                                    <div className="grid grid-cols-3 gap-4">
                                      <select
                                          value={button.if.stage}
                                          onChange={(e) =>
                                              setDialogs({
                                                ...dialogs,
                                                [selectedDialog]: {
                                                  ...dialogs[selectedDialog],
                                                  stages: {
                                                    ...dialogs[selectedDialog].stages,
                                                    [selectedStage]: {
                                                      ...dialogs[selectedDialog].stages[
                                                          selectedStage
                                                          ],
                                                      keyboard: {
                                                        ...dialogs[selectedDialog].stages[
                                                            selectedStage
                                                            ].keyboard,
                                                        buttons: {
                                                          ...dialogs[selectedDialog].stages[
                                                              selectedStage
                                                              ].keyboard.buttons,
                                                          [buttonId]: {
                                                            ...button,
                                                            if: {
                                                              ...button.if,
                                                              stage: e.target.value,
                                                            },
                                                          },
                                                        },
                                                      },
                                                    },
                                                  },
                                                },
                                              })
                                          }
                                          className="p-2 border rounded-md"
                                      >
                                        <option value="">Select Condition Stage</option>
                                        {Object.keys(dialogs[selectedDialog].stages).map(
                                            (stageId) => (
                                                <option key={stageId} value={stageId}>
                                                  {stageId}
                                                </option>
                                            )
                                        )}
                                      </select>

                                      <select
                                          value={button.if.equals}
                                          onChange={(e) =>
                                              setDialogs({
                                                ...dialogs,
                                                [selectedDialog]: {
                                                  ...dialogs[selectedDialog],
                                                  stages: {
                                                    ...dialogs[selectedDialog].stages,
                                                    [selectedStage]: {
                                                      ...dialogs[selectedDialog].stages[
                                                          selectedStage
                                                          ],
                                                      keyboard: {
                                                        ...dialogs[selectedDialog].stages[
                                                            selectedStage
                                                            ].keyboard,
                                                        buttons: {
                                                          ...dialogs[selectedDialog].stages[
                                                              selectedStage
                                                              ].keyboard.buttons,
                                                          [buttonId]: {
                                                            ...button,
                                                            if: {
                                                              ...button.if,
                                                              equals: e.target.value,
                                                            },
                                                          },
                                                        },
                                                      },
                                                    },
                                                  },
                                                },
                                              })
                                          }
                                          className="p-2 border rounded-md"
                                          disabled={!button.if.stage}
                                      >
                                        <option value="">Select Option</option>
                                        {button.if.stage &&
                                            Object.keys(
                                                dialogs[selectedDialog].stages[button.if.stage]
                                                    .keyboard.buttons
                                            ).map((optionId) => (
                                                <option key={optionId} value={optionId}>
                                                  {
                                                    dialogs[selectedDialog].stages[
                                                        button.if.stage
                                                        ].keyboard.buttons[optionId].text
                                                  }
                                                </option>
                                            ))}
                                      </select>

                                      <select
                                          value={button.if.to}
                                          onChange={(e) =>
                                              setDialogs({
                                                ...dialogs,
                                                [selectedDialog]: {
                                                  ...dialogs[selectedDialog],
                                                  stages: {
                                                    ...dialogs[selectedDialog].stages,
                                                    [selectedStage]: {
                                                      ...dialogs[selectedDialog].stages[
                                                          selectedStage
                                                          ],
                                                      keyboard: {
                                                        ...dialogs[selectedDialog].stages[
                                                            selectedStage
                                                            ].keyboard,
                                                        buttons: {
                                                          ...dialogs[selectedDialog].stages[
                                                              selectedStage
                                                              ].keyboard.buttons,
                                                          [buttonId]: {
                                                            ...button,
                                                            if: {
                                                              ...button.if,
                                                              to: e.target.value,
                                                            },
                                                          },
                                                        },
                                                      },
                                                    },
                                                  },
                                                },
                                              })
                                          }
                                          className="p-2 border rounded-md"
                                      >
                                        <option value="">Select Target Stage</option>
                                        {Object.keys(dialogs[selectedDialog].stages)
                                            .filter((stageId) => stageId !== selectedStage)
                                            .map((stageId) => (
                                                <option key={stageId} value={stageId}>
                                                  {stageId}
                                                </option>
                                            ))}
                                      </select>
                                    </div>
                                )}
                                    <select
                                        value={button.to}
                                        onChange={(e) =>
                                            setDialogs({
                                              ...dialogs,
                                              [selectedDialog]: {
                                                ...dialogs[selectedDialog],
                                                stages: {
                                                  ...dialogs[selectedDialog].stages,
                                                  [selectedStage]: {
                                                    ...dialogs[selectedDialog].stages[
                                                        selectedStage
                                                        ],
                                                    keyboard: {
                                                      ...dialogs[selectedDialog].stages[
                                                          selectedStage
                                                          ].keyboard,
                                                      buttons: {
                                                        ...dialogs[selectedDialog].stages[
                                                            selectedStage
                                                            ].keyboard.buttons,
                                                        [buttonId]: {
                                                          ...button,
                                                          to: e.target.value,
                                                        },
                                                      },
                                                    },
                                                  },
                                                },
                                              },
                                            })
                                        }
                                        className="w-full p-2 border rounded-md"
                                    >
                                      <option value="">Select Target Stage</option>
                                      {Object.keys(dialogs[selectedDialog].stages)
                                          .filter((stageId) => stageId !== selectedStage)
                                          .map((stageId) => (
                                              <option key={stageId} value={stageId}>
                                                {stageId}
                                              </option>
                                          ))}
                                    </select>

                              </div>
                          ))}
                        </div>
                      </div>
                    </div>
                )}
          </div>
        </div>
      </div>
  );
}