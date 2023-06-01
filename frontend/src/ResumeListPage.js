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
        <div>
            <p>List page</p>
            <ul>
                {list.map((r)=>(<li key={r}><ResumeListItem id={r}/></li>))}
            </ul>
        </div>
    );
};

export default ResumeListPage;
