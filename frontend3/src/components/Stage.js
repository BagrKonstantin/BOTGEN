import React from "react";
import { useDispatch } from "react-redux";
import { updateStage, deleteStage } from "../store/stageSlice";

const Stage = ({ stage }) => {
    const dispatch = useDispatch();

    const handleTextChange = (e) => {
        dispatch(updateStage({ id: stage.id, changes: { text: e.target.value } }));
    };

    return (
        <div className="border p-4 rounded-md bg-gray-100">
            <input
                type="text"
                value={stage.text}
                onChange={handleTextChange}
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
