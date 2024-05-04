import ReactDOM from "react-dom/client";
import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ChakraProvider } from "@chakra-ui/react";

import Home from "./pages/Landing/Home";
import Fetch from "./pages/Diagnose/Fetch";
import Input from "./pages/Input/Input";
import Diagnose from "./pages/Diagnose/Diagnose";
import User from "./pages/User/User";

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
		path: "/profile",
		element: "Please specify your username!",
	},
	{
		path: "/profile/:username",
		element: <User />,
	},
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<ChakraProvider>
			<RouterProvider router={router} />
		</ChakraProvider>
	</React.StrictMode>
);
