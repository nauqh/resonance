import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";

// Components
import DisplayCard from "./DisplayCard";
import UserProfile from "./UserProfile";

// Styles
import "./User.css";

interface Data {
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

const User = () => {
	const navigate = useNavigate();
	const params = useParams();

	const [data, setData] = useState<Data[]>();

	useEffect(() => {
		const fetchDataAndSetData = async () => {
			if (!data) {
				const resp = await fetch(
					`http://127.0.0.1:8000/users/${params.username}@gmail.com/diagnoses`
				);
				const jsonData = await resp.json();
				setData(jsonData);
			}
		};

		fetchDataAndSetData();
	}, [data]);

	return (
		<>
			{data ? (
				<section className="container">
					<UserProfile
						name="Dan Abrahmov"
						subtitle={params.username}
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
										playlist={item.content.playlist.name}
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
