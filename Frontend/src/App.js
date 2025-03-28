import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { addStage } from "./store/stageSlice";
import Stage from "./components/Stage";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

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
            <DndProvider backend={HTML5Backend}>
          {stages.map((stage) => (
              <Stage key={stage.id} stage={stage} />
          ))}
            </DndProvider>
      </div>

  );
};

export default App;
