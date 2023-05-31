import React from 'react';
import { useState, useEffect } from "react";
import parse from 'html-react-parser';

const ResumeList = () => {
    const [data, setData] = useState("no data");
    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/resume/1/html')
          .then((response) => response.text())
          .then((actualData) => setData(actualData));
        }, []);
    return (
        <div>
        <h2>List of books</h2> 
        {parse(data)}
        </div>
    );
};

export default ResumeList;
