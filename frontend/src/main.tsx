import ReactDOM from "react-dom/client";
import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Home from "./pages/Landing/Home";
import Fetch from "./pages/Diagnose/Fetch";
import Input from "./pages/Input/Input";
import Diagnose from "./pages/Diagnose/Diagnose";
import Receipt from "./pages/Receipt/Receipt";

import "./assets/index.css";

const router = createBrowserRouter([
	{
		path: "/",
		element: <Home />,
	},
	{
		path: "/home",
		element: <Home />,
	},
	{
		path: "/input",
		element: <Input />,
	},
	{
		path: "/diagnose",
		element: <Diagnose />,
	},
	{
		path: "/fetch",
		element: <Fetch />,
	},
	{
		path: "/receipt",
		element: <Receipt />,
	},
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);
