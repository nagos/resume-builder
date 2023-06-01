import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Logout from "./Logout";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { Link as RouterLink } from "react-router-dom";
import Paper from '@mui/material/Paper';

const defaultTheme = createTheme();
const Layout = ({children, logout}) => {
    return (
        <ThemeProvider theme={defaultTheme}>
            <CssBaseline />
            <AppBar position="relative">
                <Toolbar>
                    <Typography 
                        variant="h6" 
                        color="inherit" 
                        noWrap 
                        sx={{ flexGrow: 1, textDecoration: 'none' }} 
                        component={RouterLink} 
                        to="/"
                    >
                        Resume Builder
                    </Typography>
                    {logout && <Logout/>}
                </Toolbar>
            </AppBar>
            <Box
                component="main"
                sx={{
                    backgroundColor: (theme) =>
                    theme.palette.mode === 'light'
                        ? theme.palette.grey[100]
                        : theme.palette.grey[900],
                    flexGrow: 1,
                    height: '100vh',
                    overflow: 'auto',
                }}
            >
                <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <Box>
                            {children}
                        </Box>
                    </Paper>
                </Container>
            </Box>
        </ThemeProvider>
    );
};

export default Layout;
