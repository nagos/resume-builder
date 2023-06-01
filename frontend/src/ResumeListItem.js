import React from 'react';
import { Link } from "react-router-dom";

const ResumeListItem = ({data}) => {
    const url = `/edit/${data.id}`;
    const publicUrl = `/view/${data.id}`;
    return (
        <div>
            <Link to={url}>{data.title}</Link> (<Link to={publicUrl}>Public</Link>)
        </div>
    );
};

export default ResumeListItem;
