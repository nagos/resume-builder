import { React } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';

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
        <button onClick={logoutClick}>Logout</button>
    );
};

export default Logout;
