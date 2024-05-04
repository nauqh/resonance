import { Text, Heading, Flex, Link } from "@chakra-ui/react";
import { Card, Image } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

const DisplayCard = () => {
	return (
		<Card
			marginBottom={"1rem"}
			padding={"1rem"}
			direction={{ base: "column", sm: "row" }}
			columnGap={"2rem"}
		>
			<Image
				boxSize={{ base: "100px", lg: "150px" }}
				objectFit="cover"
				src="/homepage.png"
			/>
			<Flex direction={"column"} rowGap={"0.2rem"}>
				<Heading size={"md"} mb={"0.5rem"}>
					<Link href="http://localhost:5173/user" isExternal>
						Korean Soft Indie
						<ExternalLinkIcon mx="5px" mb="5px" />
					</Link>
				</Heading>
				<Text>Mood: soothing - soft - smooth</Text>
				<Text>Artists: Justin Bieber, Charlie Puth</Text>
				<Text>Treatment: 9</Text>
				<Text>Duration:31:50</Text>
			</Flex>
		</Card>
	);
};

export default DisplayCard;
