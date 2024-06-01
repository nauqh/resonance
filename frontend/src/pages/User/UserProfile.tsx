import { Text, Avatar, Flex, Box } from "@chakra-ui/react";

interface UserProfileProps {
	name: string;
	subtitle?: string;
	joined_at: string;
}

const UserProfile = ({ name, subtitle, joined_at }: UserProfileProps) => {
	const parsedDate = new Date(joined_at);
	return (
		<Flex
			justifyContent={"space-between"}
			width={{ base: "320px", md: "500px", lg: "580px" }}
			mt="3rem"
		>
			<Box>
				<Text
					fontSize={{ base: "1.8rem", md: "2rem", lg: "2.5rem" }}
					fontWeight="800"
					margin="1rem 0"
				>
					{name}
				</Text>
				<Text>{subtitle}</Text>
				<Text mt={"2rem"} fontSize={"0.9rem"}>
					Joined in: {parsedDate.getDate()}/{parsedDate.getMonth()}/
					{parsedDate.getFullYear()}
				</Text>
			</Box>
			<Avatar
				src="https://bit.ly/dan-abramov"
				size={{ base: "xl", lg: "2xl" }}
			/>
		</Flex>
	);
};

export default UserProfile;
