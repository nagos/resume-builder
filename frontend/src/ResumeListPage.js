import { React, useState, useEffect } from "react";
import Backend from './backend';
import ResumeListItem from "./ResumeListItem";
import Logout from "./Logout";
import { Link } from "react-router-dom";

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
            <Link to='/create'>Create</Link>
            <ul>
                {list.map((r)=>(<li key={r.id}><ResumeListItem data={r}/></li>))}
            </ul>
            <Logout/>
        </div>
    );
};

export default ResumeListPage;
