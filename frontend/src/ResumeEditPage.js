import { React, useState, useEffect } from "react";
import Backend from './backend';
import { useParams } from 'react-router-dom';
import { useNavigate } from "react-router-dom";

const ResumeEditPage = () => {
    const backend = new Backend();
    let { id } = useParams();
    const [text, setText] = useState("");
    const navigate = useNavigate();

    function resumeUpdate(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        const formJson = Object.fromEntries(formData.entries());

        const login = backend.resumeUpdate(id, formJson.text);
    }

    function resumeDelete(e) {
        e.preventDefault();
        backend.resumeDelete(id).then(() => {
            navigate("/list");
        });
    }
    
    function textChange(e) {
        setText(e.target.value);
    }

    useEffect(() => {
        backend.resumeGet(id).then((data) => {
            setText(data.text);
        })
    }, []);
    

    return (
        <form onSubmit={resumeUpdate}>
            <textarea name='text' value={text} onChange={textChange}/>
            <br/>
            <button type="submit" >Update</button>
            <button onClick={resumeDelete}>Delete</button>
        </form>
    );
};

export default ResumeEditPage;
