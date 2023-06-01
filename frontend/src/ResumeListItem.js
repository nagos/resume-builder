import React from 'react';
import { Link } from "react-router-dom";

const ResumeListItem = ({id}) => {
    const url = `/edit/${id}`;
    const publicUrl = `/view/${id}`;
    return (
        <div>
            <Link to={url}>{id}</Link> (<Link to={publicUrl}>Public</Link>)
        </div>
    );
};

export default ResumeListItem;
