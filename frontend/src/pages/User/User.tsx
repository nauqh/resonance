import { useNavigate, useParams } from "react-router-dom";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";

// Components
import DisplayCard from "./DisplayCard";
import UserProfile from "./UserProfile";

// Styles
import "./User.css";

const User = () => {
	const navigate = useNavigate();
	const params = useParams();

	return (
		<>
			<section className="container">
				<UserProfile name="Dan Abrahmov" subtitle={params.username} />

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
								color="#9395D3"
								artists="Justin Bieber, Charlie Puth"
								playlist="soft & chill korean music"
							/>
							<DisplayCard
								genre="Lo-fi Hip Hop"
								mood="chill - mellow - soothing"
								color="#3c6e71"
								artists="Eevee, Tomppabeats"
								playlist="lofi beats to relax/study to"
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
