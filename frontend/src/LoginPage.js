import { React, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';
import { Link as RouterLink } from "react-router-dom";
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Avatar from '@mui/material/Avatar';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import TextField from '@mui/material/TextField';
import Layout from "./Layout";

const defaultTheme = createTheme();

const LoginPage = () => {
    const backend = new Backend();

    function loginSend(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());

        backend.userLogin(formJson.user, formJson.password).then((login) => {
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
        <Layout>
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            
            >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                <Box component="form" onSubmit={loginSend} noValidate sx={{ mt: 1 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="user"
                        label="User Name"
                        name="user"
                        autoComplete="username"
                        autoFocus
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Sign In
                    </Button>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mb: 2 }}
                        LinkComponent={RouterLink} to="/register"
                    >
                        Register
                    </Button>
                </Box>
            </Box>
        </Layout>
    );
};

export default LoginPage;
