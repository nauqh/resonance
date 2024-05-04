import { Text, Heading, Flex, Link } from "@chakra-ui/react";
import { Card, Image } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

interface DisplayCardProps {
	genre: string;
	mood: string;
	color: string;
	artists: string;
	playlist: string;
}

const DisplayCard = ({
	genre,
	mood,
	color,
	artists,
	playlist,
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
				<Heading size={"md"} mb={"0.5rem"} color={color}>
					<Link href="http://localhost:5173">
						{genre}
						<ExternalLinkIcon mx="5px" mb="5px" />
					</Link>
				</Heading>
				<Text>Mood: {mood}</Text>
				<Text>Artists: {artists}</Text>
				<Text>Playlist: {playlist}</Text>
				<Text>Songs: 9</Text>
			</Flex>
		</Card>
	);
};

export default DisplayCard;
