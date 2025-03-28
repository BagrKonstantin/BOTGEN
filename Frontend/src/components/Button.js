import React from "react";
import { useDispatch } from "react-redux";
// import { updateStage, deleteStage } from "../store/stageSlice";

const Button = ({ button }) => {
    return (
        <div className="border p-4 rounded-md bg-gray-100">
            <input
                type="text"
                value={stage.text}
            />
            <button
            >
                Delete
            </button>
        </div>
    );
};

export default Button;
