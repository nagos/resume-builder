import { React, useState, useEffect } from "react";
import Backend from './backend';
import { useParams } from 'react-router-dom';
import parse from 'html-react-parser';
import Layout from "./Layout";

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
        <Layout>
            {parse(text)}
        </Layout>
    );
};

export default ResumeViewPage;
