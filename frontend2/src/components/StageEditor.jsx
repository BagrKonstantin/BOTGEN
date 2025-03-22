import { useBotStore } from "@/store/useBotStore";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function StageEditor({ stageId }) {
    const { stages, updateStage } = useBotStore();
    const stage = stages.find((s) => s.id === stageId);

    if (!stage) return null;

    const handleChange = (key, value) => {
        updateStage(stageId, { [key]: value });
    };

    return (
        <div className="p-4 border rounded-lg">
            <h2 className="text-xl font-bold">{stage.name}</h2>
            <Textarea
                placeholder="Enter text..."
                value={stage.text}
                onChange={(e) => handleChange("text", e.target.value)}
            />
            <Input
                type="file"
                accept="image/*"
                onChange={(e) =>
                    handleChange("image", URL.createObjectURL(e.target.files[0]))
                }
            />
            {stage.image && <img src={stage.image} alt="Preview" className="mt-2 w-40" />}
            <Button onClick={() => updateStage(stageId, { text: "" })}>Clear</Button>
        </div>
    );
}
