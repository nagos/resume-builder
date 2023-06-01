import React from 'react';
import { useNavigate } from "react-router-dom";
import Backend from './backend';

const RegisterPage = () => {
    const backend = new Backend();
    const navigate = useNavigate();

    function registerSend(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        const formJson = Object.fromEntries(formData.entries());

        const login = backend.userRegister(formJson.user, formJson.password).then((login) => {
            if (login) {
                // Переход с задержкой, что бы применились cookies
                setTimeout(()=>navigate("/list"), 1000);
            }
        });
        
    }
    return (
        <div>
            <p>Register user</p>
            <form method="post" onSubmit={registerSend}>
                <input name="user" type="text"></input>
                <input  name="password" type="password"></input>
                <button type="submit" >Login</button>
            </form>
        </div>
    );
};

export default RegisterPage;
