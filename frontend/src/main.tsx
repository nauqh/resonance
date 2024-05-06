import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ChakraProvider } from "@chakra-ui/react";

import Home from "./pages/Landing/Home";
import Fetch from "./pages/Diagnose/Fetch";
import Input from "./pages/Input/Input";
import Diagnose from "./pages/Diagnose/Diagnose";
import User from "./pages/User/User";
import ViewDiagnose from "./pages/Diagnose/ViewDiagnose";

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
	{
		path: "/profile/:username/diagnose",
		element: <ViewDiagnose />,
	},
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
	<ChakraProvider>
		<RouterProvider router={router} />
	</ChakraProvider>
);
