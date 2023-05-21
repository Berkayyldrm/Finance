import React from 'react';
import ReactDOM from 'react-dom/client';
import { FinanceProvider } from "./context/FinanceContext";
import { RouterProvider } from 'react-router-dom';
import router from './routes/router';
import './style/bootstrap-override.scss'



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
  <FinanceProvider>
    <RouterProvider router={router}/>
  </FinanceProvider>
  </>
);

