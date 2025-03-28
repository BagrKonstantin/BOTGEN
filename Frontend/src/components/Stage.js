import React from "react";

import {useState} from "react";
import {useDrag} from "react-dnd";

import Keyboard from "./Keyboard";
import {Upload} from "lucide-react";

function Button({children, onClick}) {
    return (
        <button onClick={onClick} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            {children}
        </button>
    );
}

function Input({type, accept, onChange}) {
    return (
        <input type={type} accept={accept} onChange={onChange} className="border p-2 rounded w-full"/>
    );
}

function Textarea({value, onChange, placeholder}) {
    return (
        <textarea value={value} onChange={onChange} placeholder={placeholder}
                  className="border p-2 rounded w-full h-24"/>
    );
}

function Card({children}) {
    return (
        <div className="p-4 shadow-lg rounded-xl border bg-white">{children}</div>
    );
}

export default function Stage({id}) {
    const [{isDragging}, drag] = useDrag(() => ({
        type: "STAGE",
        item: {id},
        collect: (monitor) => ({
            isDragging: !!monitor.isDragging(),
        }),
    }));

    const [text, setText] = useState("");
    const [image, setImage] = useState(null);
    const [showKeyboard, setShowKeyboard] = useState(false);

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => setImage(e.target.result);
            reader.readAsDataURL(file);
        }
    };

    return (
        <Card ref={drag} className={`p-4 shadow-lg rounded-xl ${isDragging ? "opacity-50" : ""}`}>
            <Textarea
                value={text}
                onChange={(e) => setText(e.target.value.slice(0, 10000))}
                placeholder="Enter stage text (max 10000 characters)..."
                className="w-full mb-2"
            />
            <div className="flex items-center gap-2">
                <Input type="file" accept="image/*" onChange={handleImageUpload} className="hidden"
                       id={`upload-${id}`}/>
                <label htmlFor={`upload-${id}`}
                       className="cursor-pointer flex items-center gap-2 bg-gray-200 p-2 rounded-lg hover:bg-gray-300">
                    <Upload size={16}/> Upload Image
                </label>
            </div>
            {image && <img src={image} alt="Uploaded" className="mt-2 w-full rounded-lg shadow"/>}
            <Button className="mt-4 w-full" onClick={() => setShowKeyboard(true)}>
                Add Keyboard
            </Button>
            {showKeyboard && <Keyboard/>}
        </Card>
    );
}

