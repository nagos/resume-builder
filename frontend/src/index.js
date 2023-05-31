import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import ResumeListPage from './ResumeListPage';
import ResumeEditPage from './ResumeEditPage';
import IndexPage from './IndexPage';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage/>,
  },
  {
    path: "/register",
    element: <RegisterPage/>,
  },
  {
    path: "/login",
    element: <LoginPage/>,
  },
  {
    path: "/list",
    element: <ResumeListPage/>,
  },
  {
    path: "/edit",
    element: <ResumeEditPage/>,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);