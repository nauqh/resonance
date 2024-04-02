import { useState, ChangeEvent, useEffect } from "react";
import "./Slider.css";

interface SliderProps {
	min?: number;
	max?: number;
	name: string;
	description: string;
	onSliderChange: (value: number) => void;
	value: number;
}

const Slider = ({
	min = 0,
	max = 100,
	name,
	description,
	onSliderChange,
	value,
}: SliderProps) => {
	const [sliderValue, setSliderValue] = useState(value);

	useEffect(() => {
		setSliderValue(value);
	}, [value]);

	const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
		const newValue = parseInt(event.target.value);
		setSliderValue(newValue);
		onSliderChange(newValue);
	};

	const sliderPosition = ((sliderValue - min) / (max - min)) * 100;

	return (
		<div className="slider">
			<span className="slider__header">{name}</span>

			<div className="slider__box">
				<span className="left">{min}</span>
				<div>
					<input
						type="range"
						min={min}
						max={max}
						value={sliderValue}
						className="slider__input"
						onChange={handleChange}
					/>

					<span
						className="slider-value"
						style={{ left: `${sliderPosition}%` }}
					>
						{sliderValue}
					</span>
				</div>
				<span className="right">{max}</span>
			</div>

			<p className="slider__description">{description}</p>
		</div>
	);
};

export default Slider;
