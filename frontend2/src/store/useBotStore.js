export const useBotStore = create((set) => ({
    stages: [],
    addStage: (name) =>
        set((state) => ({
            stages: [...state.stages, { id: Date.now(), name, text: "", image: null, buttons: [] }],
        })),
    updateStage: (id, data) =>
        set((state) => ({
            stages: state.stages.map((stage) =>
                stage.id === id ? { ...stage, ...data } : stage
            ),
        })),
    addButton: (stageId, button) =>
        set((state) => ({
            stages: state.stages.map((stage) =>
                stage.id === stageId
                    ? { ...stage, buttons: [...stage.buttons, button] }
                    : stage
            ),
        })),
}));
