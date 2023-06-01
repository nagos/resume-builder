import { React, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';

const ResumeEditPage = () => {
    const backend = new Backend();
    const [text, setText] = useState("");
    const navigate = useNavigate();

    function resumeCreate(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());
        backend.resumeCreate(formJson.title, formJson.text).then(() => {
            navigate("/list");
        });
    }
    
    function textChange(e) {
        setText(e.target.value);
    }

    return (
        <div>
            <p>Create resume</p>
            <form onSubmit={resumeCreate}>
                <input type="text" name="title"></input>
                <br/>
                <textarea name='text' value={text} onChange={textChange}/>
                <br/>
                <button type="submit" >Update</button>
            </form>
        </div>
    );
};

export default ResumeEditPage;
