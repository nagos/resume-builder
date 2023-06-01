import { React, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';
import { Link } from "react-router-dom";

const LoginPage = () => {
    const backend = new Backend();

    function loginSend(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        const formJson = Object.fromEntries(formData.entries());

        const login = backend.userLogin(formJson.user, formJson.password).then((login) => {
            if (login) {
                navigate("/list");
            }
        });
    }

    const navigate = useNavigate();
    useEffect(() => {
        backend.userStatus().then((login) => {
            if (login) {
                navigate("/list");
            }
        })
    }, []);
    return (
        <div>
            <p>Login page</p>
            <form method="post" onSubmit={loginSend}>
                <input name="user" type="text"></input>
                <input  name="password" type="password"></input>
                <button type="submit" >Login</button>
            </form>
            <p>
                <Link to='/register'>Register</Link>
            </p>
        </div>
    );
};

export default LoginPage;
