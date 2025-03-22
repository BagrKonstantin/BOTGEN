import { useBotStore } from "@/store/useBotStore";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function StageList() {
    const { stages, addStage } = useBotStore();

    return (
        <div className="p-4">
            <Button onClick={() => addStage(`Stage ${stages.length + 1}`)}>Add Stage</Button>
            <div className="grid grid-cols-2 gap-4 mt-4">
                {stages.map((stage) => (
                    <Card key={stage.id} className="p-4">
                        <h2 className="text-lg font-semibold">{stage.name}</h2>
                        <p>{stage.text || "No text added"}</p>
                    </Card>
                ))}
            </div>
        </div>
    );
}
