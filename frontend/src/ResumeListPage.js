import { React, useState, useEffect } from "react";
import Backend from './backend';
import { Link as RouterLink } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemSecondaryAction from "@mui/material/ListItemSecondaryAction";
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import PublicIcon from '@mui/icons-material/Public';
import Button from '@mui/material/Button';
import Layout from "./Layout";

const defaultTheme = createTheme();

const ResumeListPage = () => {
    const backend = new Backend();
    const [list, setList] = useState([]);
    useEffect(() => {
        backend.resumeList().then((data) => {
            setList(data);
        })
    }, []);
    return (
        <Layout logout='true'>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
                Resume List
            </Typography>
            <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
                {list.map((r)=>(
                    <ListItem
                        key={r.id}
                        disableGutters
                    >
                        <ListItemText>{r.title}</ListItemText>
                        <ListItemSecondaryAction>
                            <IconButton edge="end" aria-label="edit" LinkComponent={RouterLink} to={`/edit/${r.id}/`}>
                                <EditIcon />
                            </IconButton>
                            <IconButton edge="end" aria-label="public" LinkComponent={RouterLink} to={`/view/${r.id}/`}>
                                <PublicIcon />
                            </IconButton>
                        </ListItemSecondaryAction>
                    </ListItem>
                ))}
            </List>
            <Button
                type="submit"
                variant="contained"
                sx={{ mt: 3, mb: 2, mr: 2}}
                LinkComponent={RouterLink} to='/create'
                >
                    Create
            </Button>
        </Layout>
    );
};

export default ResumeListPage;
