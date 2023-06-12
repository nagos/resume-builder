import { React } from "react";
import { useNavigate } from "react-router-dom";
import Backend from './backend';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Avatar from '@mui/material/Avatar';
import LockPersonOutlinedIcon from '@mui/icons-material/LockPersonOutlined';
import TextField from '@mui/material/TextField';
import Layout from "./Layout";

const RegisterPage = () => {
    const backend = new Backend();
    const navigate = useNavigate();

    function registerSend(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());

        backend.userRegister(formJson.user, formJson.password).then((login) => {
            if (login) {
                navigate("/list");
            }
        });
        
    }
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
                    <LockPersonOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Register
                </Typography>
                <Box component="form" onSubmit={registerSend} noValidate sx={{ mt: 1 }}>
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
                        Register
                    </Button>
                </Box>
            </Box>
        </Layout>
    );
};

export default RegisterPage;
