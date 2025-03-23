import React from "react";
import { useDispatch } from "react-redux";
import { updateStage, deleteStage } from "../store/stageSlice";

const Stage = ({ stage }) => {
    const dispatch = useDispatch();


    return (
        <div className="border p-4 rounded-md bg-gray-100">
            <input
                type="text"
                value={stage.text}
                className="w-full border p-2"
            />
            <button
                onClick={() => dispatch(deleteStage(stage.id))}
                className="bg-red-500 text-white px-2 py-1 mt-2"
            >
                Delete
            </button>
        </div>
    );
};

export default Stage;
