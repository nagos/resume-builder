import { React } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';
import Button from '@mui/material/Button';

const Logout = () => {
    const backend = new Backend();
    const navigate = useNavigate();
    function logoutClick(e) {
        e.preventDefault();
        backend.userLogout().then((login) => {
            navigate("/");
        });
    }
    return (
        <Button color="inherit" onClick={logoutClick}>Logout</Button>
    );
};

export default Logout;
