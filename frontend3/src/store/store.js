import { configureStore } from "@reduxjs/toolkit";
import stageReducer from "./stageSlice";

export const store = configureStore({
    reducer: {
        stages: stageReducer,
    },
});