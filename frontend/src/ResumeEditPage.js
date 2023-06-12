import { React, useState, useEffect } from "react";
import Backend from './backend';
import { useParams } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Layout from "./Layout";

const ResumeEditPage = () => {
    const backend = new Backend();
    let { id } = useParams();
    const [text, setText] = useState("");
    const [title, setTitle] = useState("");
    const navigate = useNavigate();

    function resumeUpdate(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());

        backend.resumeUpdate(id, formJson.title, formJson.text).then(() => {
            navigate("/list");
        });
    }

    function resumeDelete(e) {
        e.preventDefault();
        backend.resumeDelete(id).then(() => {
            navigate("/list");
        });
    }
    
    function titleChange(e) {
        setTitle(e.target.value);
    }

    function textChange(e) {
        setText(e.target.value);
    }

    useEffect(() => {
        const backend = new Backend();
        backend.resumeGet(id).then((data) => {
            setText(data.text);
            setTitle(data.title);
        })
    });
    

    return (
        <Layout logout='true'>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
                Edit
            </Typography>
            <Box component="form" onSubmit={resumeUpdate} noValidate sx={{ mt: 1 }}>
                <TextField
                    margin="normal"
                    fullWidth
                    name="title"
                    label="Title"
                    type="text"
                    id="title"
                    value={title}
                    onChange={titleChange}
                />
                <TextField
                    margin="normal"
                    fullWidth
                    name="text"
                    type="text"
                    id="text"
                    multiline
                    value={text}
                    onChange={textChange}
                    minRows={10}
                />
                <Button
                    type="submit"
                    variant="contained"
                    sx={{ mt: 3, mb: 2, mr: 2}}
                >
                    Update
                </Button>
                <Button
                    type="submit"
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                    onClick={resumeDelete}
                    color="error"
                >
                    Delete
                </Button>
            </Box>
        </Layout>
    );
};

export default ResumeEditPage;
