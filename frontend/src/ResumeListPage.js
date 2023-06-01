import { React, useState, useEffect } from "react";
import Backend from './backend';
import ResumeListItem from "./ResumeListItem";
import Logout from "./Logout";

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
            <Logout/>
        </div>
    );
};

export default ResumeListPage;
