import { Text, Heading, Flex } from "@chakra-ui/react";
import { Card, Image } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

interface DisplayCardProps {
	genre: string;
	mood: string;
	color: string;
	artists: string;
	playlist: any;
	onClick?: () => void;
}

const DisplayCard = ({
	genre,
	mood,
	color,
	artists,
	playlist,
	onClick,
}: DisplayCardProps) => {
	return (
		<Card
			marginBottom={"1rem"}
			padding={"1rem"}
			direction={{ base: "column", sm: "row" }}
			columnGap={"2rem"}
			cursor={onClick ? "pointer" : "default"}
			onClick={onClick}
			_hover={{
				transform: "translateY(-5px)",
				transition: "transform 0.3s",
			}}
		>
			<Image
				boxSize={{ base: "100px", lg: "150px" }}
				objectFit="cover"
				src={playlist.images[0].url}
			/>
			<Flex direction={"column"} rowGap={"0.2rem"}>
				<Heading size={"md"} mb={"0.5rem"} color={color}>
					{genre}
					<ExternalLinkIcon mx="5px" mb="5px" />
				</Heading>
				<Text>Mood: {mood}</Text>
				<Text>Artists: {artists}</Text>
				<Text>Playlist: {playlist.name}</Text>
				<Text>Songs: 9</Text>
			</Flex>
		</Card>
	);
};

export default DisplayCard;
