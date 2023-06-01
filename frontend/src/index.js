import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import ResumeListPage from './ResumeListPage';
import ResumeEditPage from './ResumeEditPage';
import ResumeCreatePage from './ResumeCreatePage';
import ResumeViewPage from './ResumeViewPage';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage/>,
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
    path: "/edit/:id",
    element: <ResumeEditPage/>,
  },
  {
    path: "/create",
    element: <ResumeCreatePage/>,
  },
  {
    path: "/view/:id",
    element: <ResumeViewPage/>,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>
);
