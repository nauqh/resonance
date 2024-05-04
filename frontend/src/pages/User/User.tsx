import {
	Tabs,
	TabList,
	TabPanels,
	Tab,
	TabPanel,
	Card,
} from "@chakra-ui/react";

import DisplayCard from "./DisplayCard";
import UserProfile from "./UserProfile";

import "./User.css";

const User = () => {
	return (
		<>
			<section className="container">
				<UserProfile />

				<Tabs colorScheme="gray">
					<TabList>
						<Tab>Diagnosis</Tab>
						<Tab>Receipt</Tab>
					</TabList>

					<TabPanels>
						{/* Diagnosis cards */}
						<TabPanel>
							<DisplayCard />
							<DisplayCard />
						</TabPanel>

						{/* Receipt cards */}
						<TabPanel>
							<Card marginBottom={"1rem"} padding={"1rem"}></Card>
						</TabPanel>
					</TabPanels>
				</Tabs>
				<button className="user__button">Back home</button>
			</section>
		</>
	);
};

export default User;
