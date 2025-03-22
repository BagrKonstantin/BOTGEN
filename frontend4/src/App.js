import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { addStage } from "./store/stageSlice";
import Stage from "./components/Stage";

const App = () => {
  const dispatch = useDispatch();
  const stages = useSelector((state) => state.stages);

  return (
      <div className="p-5">
        <button
            onClick={() => dispatch(addStage())}
            className="bg-blue-500 text-white p-2 rounded"
        >
          Add Stage
        </button>
        <div className="mt-4 space-y-4">
          {stages.map((stage) => (
              <Stage key={stage.id} stage={stage} />
          ))}
        </div>
      </div>
  );
};

export default App;
