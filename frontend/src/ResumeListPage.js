import { React, useState, useEffect } from "react";
import Backend from './backend';
import ResumeListItem from "./ResumeListItem";

const ResumeListPage = () => {
    const backend = new Backend();
    const [list, setList] = useState([]);
    useEffect(() => {
        backend.resumeList().then((data) => {
            setList(data);
        })
    }, []);
    return (
        <p>List page
            <ul>
                {list.map((r)=>(<li><ResumeListItem id={r}/></li>))}
            </ul>
        </p>
    );
};

export default ResumeListPage;
