import { useState } from "react";
import { motion } from "framer-motion";
import { useLocation, useNavigate } from "react-router-dom";
// import { useParams } from "react-router-dom";

// Components
import Typewriter from "../../components/Typewriter/Typewriter";
import Frame from "../../components/Frame/Frame";
import Artist from "../../components/Artist/Artist";
import Playlist from "../../components/Playlist/Playlist";

import { Data } from "../User/User";

// Style
import "./Fetch.css";

const ViewDiagnose = () => {
	const location = useLocation();
	const navigate = useNavigate();
	// const params = useParams();

	const [firstWriterComplete, setFirstWriterComplete] = useState(false);
	const [secondWriterComplete, setSecondWriterComplete] = useState(false);

	const data: Data = location.state.data;

	const handleButtonClick = () => {
		// navigate(`/profile/${params.username}`);
		navigate(-1);
	};

	return (
		<>
			{data ? (
				<>
					<section className="container">
						<motion.h1
							className="result__title"
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							transition={{ duration: 1, delay: 0.5 }}
							style={{
								color: data.content.color,
							}}
						>
							{data.content.mood}
						</motion.h1>

						<motion.img
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							transition={{ duration: 1, delay: 2 }}
							style={{
								margin: "auto",
							}}
							src="/music_banner.png"
							width={500}
						/>
					</section>
					<motion.section
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ duration: 1, delay: 3 }}
						className="container"
						id="description"
					>
						<Typewriter
							text={data.content.characteristics[0]}
							delay={30}
							onComplete={() => {
								setFirstWriterComplete(true);
							}}
						/>
						{firstWriterComplete && (
							<Typewriter
								text={data.content.characteristics[1]}
								delay={30}
								onComplete={() => {
									setSecondWriterComplete(true);
								}}
							/>
						)}
					</motion.section>

					{secondWriterComplete && (
						<motion.div
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							transition={{ duration: 1, delay: 1 }}
						>
							<section className="container">
								<h1 className="result__header">
									Famous artists represent your music taste
								</h1>

								{data.content.artists.map(
									(artist: any, index: any) => (
										<Artist
											key={index}
											img={artist.img}
											name={artist.name}
											content={artist.content}
											color={data.content.color}
										/>
									)
								)}
							</section>

							<section className="container">
								<h1 className="result__header">
									This playlist might be your cup of tea
								</h1>
								<Playlist
									playlist={data.content.playlist}
									color={data.content.color}
								/>
							</section>

							<section className="container">
								<h1 className="result__header">
									Here are the songs that are tailored for you
								</h1>
								<Frame
									trackIds={data.content.tracks.map(
										(track) => track.id
									)}
								/>
							</section>

							<section className="container">
								<button
									className="button-alter"
									onClick={handleButtonClick}
								>
									Back to profile
								</button>
							</section>
						</motion.div>
					)}
				</>
			) : null}
		</>
	);
};

export default ViewDiagnose;
