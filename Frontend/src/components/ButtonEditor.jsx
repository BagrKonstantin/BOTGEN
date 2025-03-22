import { useBotStore } from "@/store/useBotStore";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export default function ButtonEditor({ stageId }) {
    const { stages, addButton } = useBotStore();
    const [buttonText, setButtonText] = useState("");
    const [targetStage, setTargetStage] = useState(null);

    return (
        <div>
            <Input placeholder="Button text" value={buttonText} onChange={(e) => setButtonText(e.target.value)} />
            <Select onChange={(e) => setTargetStage(e.target.value)}>
                <option value="">Select Stage</option>
                {stages
                    .filter((s) => s.id !== stageId)
                    .map((s) => (
                        <option key={s.id} value={s.id}>
                            {s.name}
                        </option>
                    ))}
            </Select>
            <Button onClick={() => addButton(stageId, { text: buttonText, target: targetStage })}>
                Add Button
            </Button>
        </div>
    );
}
