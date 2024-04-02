import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

// Components
import TextInput from "../../components/TextInput/TextInput";
import Features from "../../assets/data/features.json";
import Slider from "../../components/Slider/Slider";
import WorkFilter from "../../components/Filter/WorkFilter";
import GenreGrid from "../../components/GenreGrid";
import SelectBox from "../../components/SelectBox/SelectBox";

type FilterKey = "Upbeat" | "Ambient" | "Anxious" | "Inspiring";

const Input = () => {
	const navigate = useNavigate();

	const [sliderValues, setSliderValues] = useState({
		Danceability: 50,
		Energy: 50,
		Instrumentalness: 50,
		Loudness: -10,
		Valence: 40,
	});
	const [notes, setNotes] = useState("");
	const [genre, setGenre] = useState<FilterKey>();
	const [_, setSelectedOption] = useState("");

	const handleFilterChange = (filter: FilterKey) => {
		setSliderValues(Features[filter]);
		setGenre(filter);
	};

	const handleSliderChange = (name: string, value: number) => {
		setSliderValues((prevValues) => ({
			...prevValues,
			[name]: value,
		}));
	};

	const handleButtonClick = () => {
		const features = Object.fromEntries(
			Object.entries(sliderValues).map(([key, value]) => [
				key,
				value / 100,
			])
		);
		console.log(features);
		console.log(notes);
		console.log(genre);
		window.location.href = "https://nauqh.github.io/error";
		navigate("/fetch", {
			state: {
				description: notes ? notes : "soft korean pop indie",
				genre: genre,
			},
		});
	};

	const handleDiagnoseSelect = (text: string) => {
		navigate("/diagnose", { state: { text } });
	};

	return (
		<motion.div
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			transition={{ duration: 1, delay: 0.5 }}
		>
			<section
				className="container"
				style={{
					marginTop: "2rem",
					marginBottom: 0,
				}}
			>
				<h1
					style={{
						fontSize: "1rem",
						marginBottom: "2rem",
						textAlign: "center",
					}}
				>
					Pick a genre from our popular diagnoses
				</h1>
				<GenreGrid onDiagnoseSelect={handleDiagnoseSelect} />
			</section>

			<section className="container">
				<h1
					style={{
						fontSize: "1rem",
						margin: "2rem 0",
						padding: "0 2rem",
						textAlign: "center",
					}}
				>
					Or choose a mood and custom your own preference
				</h1>
				<WorkFilter onFilterChange={handleFilterChange} />
			</section>

			<section
				className="container"
				style={{
					marginBottom: 0,
				}}
			>
				<Slider
					name="Danceability"
					description="Danceability describes how suitable a track is for dancing based on a combination of musical elements"
					onSliderChange={(value) =>
						handleSliderChange("Danceability", value)
					}
					value={sliderValues.Danceability}
				/>
				<Slider
					name="Energy"
					description="Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity."
					onSliderChange={(value) =>
						handleSliderChange("Energy", value)
					}
					value={sliderValues.Energy}
				/>
				<Slider
					name="Instrumentalness"
					description="Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context."
					onSliderChange={(value) =>
						handleSliderChange("Instrumentalness", value)
					}
					value={sliderValues.Instrumentalness}
				/>

				<Slider
					min={-60}
					max={0}
					name="Loudness"
					description="Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude)."
					onSliderChange={(value) =>
						handleSliderChange("Loudness", value)
					}
					value={sliderValues.Loudness}
				/>
				<Slider
					min={0}
					max={100}
					name="Valence"
					description="Valence describes the positiveness conveyed by a track. Tracks with high valence sound more positive, while tracks with low valence sound more negative."
					onSliderChange={(value) =>
						handleSliderChange("Valence", value)
					}
					value={sliderValues.Valence}
				/>
				<SelectBox
					labell="Choose an option:"
					labelr="Year range"
					options={["Option 1", "Option 2", "Option 3", "Option 4"]}
					onChange={(selectedOption) => {
						setSelectedOption(selectedOption);
					}}
				/>
				<TextInput
					label="Notes"
					placeholder="E.g. Some soft chill korean indie"
					value={notes}
					onChange={(text: string) => {
						setNotes(text);
					}}
				/>
			</section>

			<footer
				className="container"
				style={{
					marginBottom: "5rem",
				}}
			>
				<div className="button-alter" onClick={handleButtonClick}>
					Prescribe me new songs
				</div>
			</footer>
		</motion.div>
	);
};

export default Input;
