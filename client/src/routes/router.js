import {createBrowserRouter} from "react-router-dom";
import Home from "../pages/Home";
import Authentication from "../pages/Authentication"
import SingleCompanyPage from "../pages/SingleCompanyPage";
const router = createBrowserRouter([
    {
        path: "/",
        children: [
          {
            index: true,
            element: <Home />,
          },
          {
            path: ":name",
            element: <SingleCompanyPage />,
          },
        ],
      },
      {
        path: "/authentication",
        element: <Authentication/>
      }
])
export default router;