import { Text, Heading, Flex, Link } from "@chakra-ui/react";
import { Card, Image } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

interface DisplayCardProps {
	genre: string;
	mood: string;
	artists: string;
	treatment: string;
	duration: string;
}

const DisplayCard = ({
	genre,
	mood,
	artists,
	treatment,
	duration,
}: DisplayCardProps) => {
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
					<Link href="http://localhost:5173">
						{genre}
						<ExternalLinkIcon mx="5px" mb="5px" />
					</Link>
				</Heading>
				<Text>Mood: {mood}</Text>
				<Text>Artists: {artists}</Text>
				<Text>Treatment: {treatment}</Text>
				<Text>Duration: {duration}</Text>
			</Flex>
		</Card>
	);
};

export default DisplayCard;
