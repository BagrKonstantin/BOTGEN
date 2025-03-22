import { createSlice } from "@reduxjs/toolkit";
import { v4 as uuidv4 } from "uuid";

const stageSlice = createSlice({
    name: "stages",
    initialState: [],
    reducers: {
        addStage: (state) => {
            state.push({ id: uuidv4(), text: "New Stage", image: null, buttons: [] });
        },
        updateStage: (state, action) => {
            const { id, changes } = action.payload;
            const stage = state.find((s) => s.id === id);
            if (stage) {
                Object.assign(stage, changes);
            }
        },
        deleteStage: (state, action) => {
            return state.filter((s) => s.id !== action.payload);
        },
    },
});

export const { addStage, updateStage, deleteStage } = stageSlice.actions;
export default stageSlice.reducer;
