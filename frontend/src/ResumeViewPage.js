import { React, useState, useEffect } from "react";
import Backend from './backend';
import { useParams } from 'react-router-dom';
import parse from 'html-react-parser';

const ResumeViewPage = () => {
    const backend = new Backend();
    let { id } = useParams();
    const [text, setText] = useState("");

    useEffect(() => {
        backend.resumeGetView(id).then((data) => {
            setText(data);
        })
    }, []);

    return (
        <div>{parse(text)}</div>
    );
};

export default ResumeViewPage;
