import { useNavigate } from "react-router-dom";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";

// Components
import DisplayCard from "./DisplayCard";
import UserProfile from "./UserProfile";

// Styles
import "./User.css";

const User = () => {
	const navigate = useNavigate();

	return (
		<>
			<section className="container">
				<UserProfile />

				<Tabs colorScheme="gray" minHeight="480px">
					<TabList>
						<Tab>Diagnosis</Tab>
						<Tab>Receipt</Tab>
					</TabList>

					<TabPanels>
						{/* Diagnosis cards */}
						<TabPanel>
							<DisplayCard
								genre="Korean Soft Indie"
								mood="soothing - soft - smooth"
								artists="Justin Bieber, Charlie Puth"
								treatment="9"
								duration="31:50"
							/>
							<DisplayCard
								genre="Lo-fi Hip Hop"
								mood="chill - mellow - soothing"
								artists="Eevee, Tomppabeats"
								treatment="9"
								duration="23:30"
							/>

							{/* <DisplayCard /> */}
						</TabPanel>

						{/* Receipt cards */}
						<TabPanel></TabPanel>
					</TabPanels>
				</Tabs>

				<button
					className="user__button"
					onClick={() => {
						navigate("/home");
					}}
				>
					Back home
				</button>
			</section>
		</>
	);
};

export default User;
