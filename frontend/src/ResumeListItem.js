import React from 'react';
import { Link } from "react-router-dom";

const ResumeListItem = ({id}) => {
    const url = `/edit/${id}`;
    console.log(url);
    return (
        <Link to={url}>{id}</Link>
    );
};

export default ResumeListItem;
