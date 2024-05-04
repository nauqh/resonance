import { Text, Avatar, Flex, Box } from "@chakra-ui/react";

const UserProfile = () => {
	return (
		<Flex columnGap={{ base: "5rem", md: "10rem", lg: "15rem" }} mt="5rem">
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
	);
};

export default UserProfile;
