import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Box, Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import { Alert, AlertTitle, AlertDescription } from "@chakra-ui/react";

// Components
import DisplayCard from "./DisplayCard";
import UserProfile from "./UserProfile";

// Styles
import "./User.css";

export interface Data {
	content: {
		genre: string;
		mood: string;
		color: string;
		characteristics: string[];
		artists: {
			name: string;
			img: string;
			id: string;
			content: string;
		}[];
		tracks: {
			id: string;
			name: string;
			artist: string;
			duration: string;
		}[];
		playlist: any;
	};
}

interface User {
	email: string;
	name: string;
	created_at: string;
}

const User = () => {
	const navigate = useNavigate();
	const params = useParams();

	const [data, setData] = useState<Data[]>();
	const [user, setUser] = useState<User>();

	useEffect(() => {
		const fetchData = async () => {
			if (!data) {
				const dataResp = await fetch(
					`https://web-production-460c1.up.railway.app/users/${params.username}@gmail.com/diagnoses`
				);
				const userDataResp = await fetch(
					`https://web-production-460c1.up.railway.app/users/${params.username}@gmail.com`
				);

				const jsonData = await dataResp.json();
				const jsonUser = await userDataResp.json();

				setData(jsonData);
				setUser(jsonUser);
			}
		};

		fetchData();
	}, [data, user]);

	return (
		<>
			{data && user ? (
				<section className="container">
					<Alert
						mt={"1rem"}
						colorScheme="gray"
						width={{ base: "320px", md: "500px", lg: "580px" }}
					>
						<Box bg={"transparent"}>
							<AlertTitle bg={"transparent"}>🚧 Note!</AlertTitle>
							<AlertDescription bg={"transparent"}>
								The following feature is currently in
								development. Below is a draft of the user
								profile.
							</AlertDescription>
						</Box>
					</Alert>
					<UserProfile
						name={user.name}
						subtitle={params.username}
						joined_at={user.created_at}
					/>

					<Tabs colorScheme="gray" minHeight="480px">
						<TabList>
							<Tab>Diagnosis</Tab>
							<Tab>Receipt</Tab>
						</TabList>

						<TabPanels>
							{/* Diagnosis cards */}
							<TabPanel>
								{data.map((item, index) => (
									<DisplayCard
										key={index}
										genre={item.content.genre}
										mood={item.content.mood}
										color={item.content.color}
										artists={item.content.artists
											.map((artist) => artist.name)
											.join(", ")}
										playlist={item.content.playlist}
										onClick={() => {
											navigate(
												`/profile/${params.username}/diagnose`,
												{
													state: {
														data: data[index],
													},
												}
											);
										}}
									/>
								))}
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
			) : null}
		</>
	);
};

export default User;
