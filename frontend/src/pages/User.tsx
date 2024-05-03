import { Text, Avatar, Flex, Box } from "@chakra-ui/react";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import { Card, Image } from "@chakra-ui/react";

const User = () => {
	return (
		<section className="container">
			<Flex
				columnGap={{ base: "5rem", md: "10rem", lg: "15rem" }}
				mt="5rem"
			>
				<Box>
					<Text
						fontSize={{ base: "1.8rem", md: "2rem", lg: "2.5rem" }}
						fontWeight="800"
						margin="1rem 0"
					>
						Dan Abrahmov
					</Text>
					<Text fontSize="0.9rem"> In love with React & Next</Text>
				</Box>
				<Avatar
					src="https://bit.ly/dan-abramov"
					size={{ base: "xl", lg: "2xl" }}
				/>
			</Flex>
			<Tabs colorScheme="gray">
				<TabList>
					<Tab>Diagnosis</Tab>
					<Tab>Receipt</Tab>
				</TabList>

				<TabPanels>
					<TabPanel>
						<Card
							marginBottom={"1rem"}
							padding={"1rem"}
							bg={"#fafafa"}
						>
							<Image
								boxSize={{ base: "100px", lg: "150px" }}
								objectFit="cover"
								src="/homepage.png"
							/>
						</Card>
					</TabPanel>

					<TabPanel>
						<Card
							marginBottom={"1rem"}
							padding={"1rem"}
							bg={"#fafafa"}
						></Card>
					</TabPanel>
				</TabPanels>
			</Tabs>
		</section>
	);
};

export default User;
